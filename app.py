import gradio as gr
import pandas as pd

from filters import districts, fort_types, difficulties, seasons, conditions, df, apply_filters, go_to_previous_page, go_to_next_page
from helper_functions import get_fort_image, format_value

# Detail page logic
def show_detail_page(fort_id):
    if fort_id is None or pd.isna(fort_id):
        return gr.update(visible=True), gr.update(visible=False), None, ""

    fort_match = df[df['fort_id'] == int(fort_id)]
    if fort_match.empty:
        return gr.update(visible=True), gr.update(visible=False), None, "Fort not found"

    fort = fort_match.iloc[0]
    details = f"""Fort Name: {fort['name']}
                District: {fort['district']}
                Type: {fort['type']}
                Elevation: {fort['elevation_m']} meters
                Current Condition: {fort['current_condition']}
                Trek Difficulty: {fort['trek_difficulty']}
                Best Season: {fort['best_season']}
                Notes: {format_value(fort['notes'], 'No additional information available')}"""
    
    return (
        gr.update(visible=False),
        gr.update(visible=True),
        get_fort_image(fort['name']),
        details
    )

# UI
with gr.Blocks(title="Fort Recommender") as app:

    current_page = gr.State(value=1)

    # Main page
    with gr.Column(visible=True) as main_page:

        gr.Markdown("# 🏰 Fort Recommender")

        with gr.Row():
            district_dropdown = gr.Dropdown(
                choices=["Select District", "All Districts"] + districts,
                value="Select District", label="District", scale=3
            )
            filter_btn = gr.Button("🔍 Filters", scale=1)

        