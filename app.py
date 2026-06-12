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

    details = (
    f"Fort Name: {fort['name']}\n"
    f"District: {fort['district']}\n"
    f"Type: {fort['type']}\n"
    f"Elevation: {fort['elevation_m']} meters\n"
    f"Current Condition: {fort['current_condition']}\n"
    f"Trek Difficulty: {fort['trek_difficulty']}\n"
    f"Best Season: {fort['best_season']}\n"
    f"Notes: {format_value(fort['notes'], 'No additional information available')}"
    )
    
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

        # Filter panel
        with gr.Column(visible=False) as filter_panel:
            gr.Markdown("### Filter Options")
            type_checkbox       = gr.CheckboxGroup(choices=fort_types,   label="Fort Type")
            difficulty_checkbox = gr.CheckboxGroup(choices=difficulties, label="Trek Difficulty")
            season_checkbox     = gr.CheckboxGroup(choices=seasons,      label="Best Season")
            condition_checkbox  = gr.CheckboxGroup(choices=conditions,   label="Current Condition")
            with gr.Row():
                apply_filter_btn = gr.Button("Apply Filters", variant="primary")
                close_filter_btn = gr.Button("Close")

        gr.Markdown("---")

        with gr.Column(visible=True) as welcome_message:
            gr.Markdown("## 👋 Welcome to Fort Recommender!\n\nPlease select a district to view fort recommendations.")

        with gr.Column(visible=False) as fort_cards_section:

            # Cards — rows of 3
            card_data = []
            for row in range(2):
                with gr.Row():
                    for col in range(3):
                        with gr.Column() as container:
                            img  = gr.Image(label="Fort Image", height=200, interactive=False, type="filepath")
                            name = gr.Textbox(value="", interactive=False, show_label=False)
                            desc = gr.Textbox(value="", interactive=False, lines=5, show_label=False)
                            fid  = gr.Number(visible=False, value=None)
                            btn  = gr.Button("View Details", variant="primary", size="sm")
                        card_data.append((container, img, name, desc, fid, btn))

            # Unpack for event wiring
            (card1_container, card1_image, card1_name, card1_desc, card1_id, card1_btn,
             card2_container, card2_image, card2_name, card2_desc, card2_id, card2_btn,
             card3_container, card3_image, card3_name, card3_desc, card3_id, card3_btn,
             card4_container, card4_image, card4_name, card4_desc, card4_id, card4_btn,
             card5_container, card5_image, card5_name, card5_desc, card5_id, card5_btn,
             card6_container, card6_image, card6_name, card6_desc, card6_id, card6_btn) = [
                item for card in card_data for item in card
            ]

            with gr.Row():
                prev_btn  = gr.Button("◀ Previous", size="sm")
                page_info = gr.Textbox(value="Page 1", interactive=False, show_label=False)
                next_btn  = gr.Button("Next ▶", size="sm")

    # Detail page
    with gr.Column(visible=False) as detail_page:
        gr.Markdown("# 🏰 Fort Details")
        back_btn     = gr.Button("◀ Back to List", variant="secondary")
        detail_image = gr.Image(label="Fort Image", height=400, interactive=False, type="filepath")
        detail_text  = gr.Textbox(value="", interactive=False, lines=30, show_label=False)

    # Filter outputs list
    filter_outputs = [
        card1_container, card1_image, card1_name, card1_desc, card1_id,
        card2_container, card2_image, card2_name, card2_desc, card2_id,
        card3_container, card3_image, card3_name, card3_desc, card3_id,
        card4_container, card4_image, card4_name, card4_desc, card4_id,
        card5_container, card5_image, card5_name, card5_desc, card5_id,
        card6_container, card6_image, card6_name, card6_desc, card6_id,
        page_info, current_page, prev_btn, next_btn,
        welcome_message, fort_cards_section
    ]

    filter_inputs = [
        district_dropdown, type_checkbox, difficulty_checkbox,
        season_checkbox, condition_checkbox, current_page
    ]

    # UI Event Handlers
    filter_btn.click(fn=lambda: gr.update(visible=True),  outputs=filter_panel)
    close_filter_btn.click(fn=lambda: gr.update(visible=False), outputs=filter_panel)

    apply_filter_btn.click(
        fn=apply_filters, inputs=filter_inputs, outputs=filter_outputs
    ).then(fn=lambda: gr.update(visible=False), outputs=filter_panel)

    district_dropdown.change(fn=apply_filters, inputs=filter_inputs, outputs=filter_outputs)

    prev_btn.click(fn=go_to_previous_page, inputs=current_page, outputs=current_page).then(
        fn=apply_filters, inputs=filter_inputs, outputs=filter_outputs
    )
    next_btn.click(fn=go_to_next_page, inputs=current_page, outputs=current_page).then(
        fn=apply_filters, inputs=filter_inputs, outputs=filter_outputs
    )

    detail_outputs = [main_page, detail_page, detail_image, detail_text]
    for container, img, name, desc, fid, btn in card_data:
        btn.click(fn=show_detail_page, inputs=fid, outputs=detail_outputs)

    back_btn.click(
        fn=lambda: (gr.update(visible=True), gr.update(visible=False)),
        outputs=[main_page, detail_page]
    )

# Launch
if __name__ == "__main__":
    app.launch(theme=gr.themes.Soft(), 
               share=True,
               server_name="127.0.0.1", 
               server_port=7860, show_error=True)