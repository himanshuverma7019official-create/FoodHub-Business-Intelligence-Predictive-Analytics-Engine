import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title='FoodHub BI Dashboard',
    page_icon='🍽️',
    layout='wide',
)

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]

    numeric_cols = [
        'bill_subtotal', 'packaging_charges', 'restaurant_discount_(promo)',
        'restaurant_discount_(flat_offs,_freebies_&_others)', 'gold_discount',
        'brand_pack_discount', 'total', 'rating', 'kpt_duration_(minutes)',
        'rider_wait_time_(minutes)'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    if 'distance' in df.columns:
        df['distance_km'] = (
            df['distance']
            .astype(str)
            .str.replace('km', '', regex=False)
            .str.replace('<', '0.5', regex=False)
            .astype(float, errors='ignore')
        )

    if 'order_placed_at' in df.columns:
        df['order_placed_at'] = pd.to_datetime(df['order_placed_at'], errors='coerce')
        df['day_of_week'] = df['order_placed_at'].dt.day_name()
        df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday'])

    if 'kpt_duration_(minutes)' in df.columns:
        df['prep_time_minutes'] = df['kpt_duration_(minutes)']
    if 'rider_wait_time_(minutes)' in df.columns:
        df['delivery_time_minutes'] = df['rider_wait_time_(minutes)']

    if 'prep_time_minutes' in df.columns and 'delivery_time_minutes' in df.columns:
        df['total_time_minutes'] = df['prep_time_minutes'] + df['delivery_time_minutes']
    elif 'total' in df.columns and 'delivery_time_minutes' in df.columns:
        df['total_time_minutes'] = df['delivery_time_minutes']

    if 'total' in df.columns and 'cost_of_the_order' not in df.columns:
        df['cost_of_the_order'] = df['total']

    if 'cuisine_type' not in df.columns and 'items_in_order' in df.columns:
        df['cuisine_type'] = (
            df['items_in_order']
            .astype(str)
            .str.split(',')
            .str[0]
            .str.lower()
        )

    return df


def format_currency(value: float) -> str:
    return f'₹{value:,.2f}' if not np.isnan(value) else 'N/A'


def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header('Dashboard filters')
    if 'city' in df.columns:
        cities = sorted(df['city'].dropna().unique())
        selected_cities = st.sidebar.multiselect('City', cities, default=cities[:3])
        if selected_cities:
            df = df[df['city'].isin(selected_cities)]

    if 'order_status' in df.columns:
        statuses = sorted(df['order_status'].dropna().unique())
        selected_status = st.sidebar.multiselect('Order status', statuses, default=['Delivered'] if 'Delivered' in statuses else statuses[:2])
        if selected_status:
            df = df[df['order_status'].isin(selected_status)]

    if 'restaurant_name' in df.columns:
        all_restaurants = sorted(df['restaurant_name'].dropna().unique())
        selected_restaurants = st.sidebar.multiselect('Top restaurants', all_restaurants, default=all_restaurants[:5])
        if selected_restaurants:
            df = df[df['restaurant_name'].isin(selected_restaurants)]

    st.sidebar.markdown('---')
    st.sidebar.markdown('Built with Streamlit for FoodHub business insights')
    return df


def main() -> None:
    st.title('FoodHub Business Intelligence Dashboard')
    st.markdown(
        'Monitor orders, delivery performance, customer trends, and restaurant quality in one polished dashboard.'
    )

    data_path = 'foodhub_data.csv'
    df = load_data(data_path)
    df = filter_data(df)

    total_orders = len(df)
    delivered_orders = df[df['order_status'].str.contains('delivered', case=False, na=False)].shape[0] if 'order_status' in df.columns else 0
    avg_order_value = df['cost_of_the_order'].mean()
    avg_rating = df['rating'].mean()
    avg_prep = df['prep_time_minutes'].mean()
    avg_delivery = df['delivery_time_minutes'].mean()
    avg_total_time = df['total_time_minutes'].mean()
    slow_prep_pct = (
        (df['prep_time_minutes'] > df['prep_time_minutes'].median()).mean() * 100
        if 'prep_time_minutes' in df.columns else np.nan
    )
    top_cuisine = df['cuisine_type'].mode().iloc[0] if 'cuisine_type' in df.columns and not df['cuisine_type'].mode().empty else 'N/A'
    top_restaurant = df['restaurant_name'].mode().iloc[0] if 'restaurant_name' in df.columns and not df['restaurant_name'].mode().empty else 'N/A'

    header1, header2, header3, header4 = st.columns([1.2, 1.2, 1.2, 1.2])
    header1.metric('Total orders', f'{total_orders:,}')
    header2.metric('Delivered orders', f'{delivered_orders:,}')
    header3.metric('Avg order value', format_currency(avg_order_value))
    header4.metric('Avg rating', f'{avg_rating:.2f}' if not np.isnan(avg_rating) else 'N/A')

    header5, header6, header7, header8 = st.columns([1.2, 1.2, 1.2, 1.2])
    header5.metric('Avg prep time (min)', f'{avg_prep:.1f}' if not np.isnan(avg_prep) else 'N/A')
    header6.metric('Avg delivery wait (min)', f'{avg_delivery:.1f}' if not np.isnan(avg_delivery) else 'N/A')
    header7.metric('Avg fulfillment time (min)', f'{avg_total_time:.1f}' if not np.isnan(avg_total_time) else 'N/A')
    header8.metric('Slow prep rate', f'{slow_prep_pct:.1f}%' if not np.isnan(slow_prep_pct) else 'N/A')

    st.markdown('---')
    st.subheader('Performance overview')

    col1, col2 = st.columns([2, 1])
    with col1:
        if 'day_of_week' in df.columns:
            orders_by_day = df['day_of_week'].value_counts().reindex([
                'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
            ]).fillna(0)
            fig = px.bar(
                x=orders_by_day.index,
                y=orders_by_day.values,
                labels={'x': 'Day of Week', 'y': 'Orders'},
                title='Orders by Day of Week',
                color=orders_by_day.values,
                color_continuous_scale='Blues',
            )
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
        else:
            st.info('Day of week data not available.')

        if 'distance_km' in df.columns:
            distance_counts = df['distance_km'].fillna(0).round(1).value_counts().sort_index()
            fig = px.bar(
                x=distance_counts.index,
                y=distance_counts.values,
                labels={'x': 'Distance (km)', 'y': 'Orders'},
                title='Delivery Distance Distribution',
                color=distance_counts.values,
                color_continuous_scale='Reds',
            )
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
        else:
            st.info('Distance data not available.')

    with col2:
        info_text = f"""
### Top insights
- **Top cuisine:** {str(top_cuisine).title()}
- **Top restaurant:** {str(top_restaurant)}
- **Unique customer count:** {df['customer_id'].nunique() if 'customer_id' in df.columns else 'N/A'}
- **Unique restaurants:** {df['restaurant_name'].nunique() if 'restaurant_name' in df.columns else 'N/A'}
"""
        st.markdown(info_text)

        if 'cuisine_type' in df.columns:
            top_cuisines = df['cuisine_type'].value_counts().head(6)
            fig = px.pie(
                values=top_cuisines.values,
                names=top_cuisines.index.str.title(),
                title='Top Cuisine Types',
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})

    st.markdown('---')

    col3, col4 = st.columns(2)
    with col3:
        if 'restaurant_name' in df.columns:
            top_restaurants = df['restaurant_name'].value_counts().head(10)
            fig = px.bar(
                x=top_restaurants.index,
                y=top_restaurants.values,
                labels={'x': 'Restaurant', 'y': 'Order Count'},
                title='Top Restaurants by Orders',
                color=top_restaurants.values,
                color_continuous_scale='Viridis',
            )
            fig.update_layout(xaxis_tickangle=-45, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
        else:
            st.info('Restaurant data not available.')

    with col4:
        if 'rating' in df.columns:
            rating_counts = df['rating'].value_counts().sort_index()
            fig = px.bar(
                x=rating_counts.index,
                y=rating_counts.values,
                labels={'x': 'Rating', 'y': 'Count'},
                title='Rating Distribution',
                color=rating_counts.values,
                color_continuous_scale='Greens',
            )
            fig.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})
        else:
            st.info('Rating data not available.')

    st.markdown('---')
    with st.expander('Show dataset sample and details', expanded=True):
        st.write(df.head(15))
        st.write('### Dataset shape and column summary')
        st.write(df.describe(include='all').transpose())

    st.caption('FoodHub BI Dashboard | Static charts enabled for touch-friendly viewing.')


if __name__ == '__main__':
    main()
