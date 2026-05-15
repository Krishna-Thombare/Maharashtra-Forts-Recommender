import gradio as gr
from helper_functions import get_fort_image, get_fort_description

import pandas as pd

df = pd.read_csv('data_cleaned.csv')

districts  = sorted(df['district'].unique().tolist())
fort_types = sorted(df['type'].unique().tolist())
difficulties = ['Easy', 'Medium', 'Hard']
seasons    = sorted(df['best_season'].unique().tolist())
conditions = sorted(df['current_condition'].unique().tolist())

FORTS_PER_PAGE = 6

def apply_filters(district, fort_type, difficulty, season, condition, current_page):

    # No district selected
    if not district or district == "Select District":
        outputs = []
        for _ in range(FORTS_PER_PAGE):
            outputs.extend([gr.update(visible=False), None, "", "", None])
        outputs.extend([
            "Please select a district to view forts",
            1,
            gr.update(interactive=False),
            gr.update(interactive=False),
            gr.update(visible=True),   # welcome_message
            gr.update(visible=False)   # fort_cards_section
        ])
        return outputs

    # Filters
    filtered_df = df.copy()

    if district != "All Districts":
        filtered_df = filtered_df[filtered_df['district'] == district]

    if fort_type:
        filtered_df = filtered_df[filtered_df['type'].isin(fort_type)]

    if difficulty:
        filtered_df = filtered_df[filtered_df['trek_difficulty'].isin(difficulty)]

    if season:
        filtered_df = filtered_df[
            filtered_df['best_season'].apply(lambda x: any(s in x for s in season))
        ]

    if condition:
        filtered_df = filtered_df[filtered_df['current_condition'].isin(condition)]

    filtered_df = filtered_df.sort_values('name').reset_index(drop=True)

    # No results
    if filtered_df.empty:
        outputs = []
        for _ in range(FORTS_PER_PAGE):
            outputs.extend([gr.update(visible=False), None, "", "", None])
        message = (
            "No forts available with selected filters."
            if district == "All Districts"
            else f"No forts available in {district} with selected filters."
        )
        outputs.extend([
            message, 1,
            gr.update(interactive=False),
            gr.update(interactive=False),
            gr.update(visible=False),
            gr.update(visible=True)
        ])
        return outputs

    # Pagination 
    total_forts  = len(filtered_df)
    total_pages  = max(1, (total_forts + FORTS_PER_PAGE - 1) // FORTS_PER_PAGE)
    page         = max(1, min(current_page, total_pages))
    start_idx    = (page - 1) * FORTS_PER_PAGE
    page_forts   = filtered_df.iloc[start_idx : start_idx + FORTS_PER_PAGE]

    # Build card outputs 
    outputs = []
    for i in range(FORTS_PER_PAGE):
        if i < len(page_forts):
            fort = page_forts.iloc[i]
            outputs.extend([
                gr.update(visible=True),
                get_fort_image(fort['name']),
                fort['name'],
                get_fort_description(fort),
                fort['fort_id']
            ])
        else:
            outputs.extend([gr.update(visible=False), None, "", "", None])

    outputs.extend([
        f"Page {page} of {total_pages} | Total Forts: {total_forts}",
        page,
        gr.update(interactive=page > 1),
        gr.update(interactive=page < total_pages),
        gr.update(visible=False),  # welcome_message
        gr.update(visible=True)    # fort_cards_section
    ])
    return outputs

def go_to_previous_page(current_page):
    return max(1, current_page - 1)

def go_to_next_page(current_page):
    return current_page + 1