import full_calendar_component as fcc
from dash import *
from typing import Any, Dict, List

import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from datetime import datetime, date, timedelta
import dash_quill

app = Dash(__name__, prevent_initial_callbacks=True)

quill_mods = [
    [{"header": "1"}, {"header": "2"}, {"font": []}],
    [{"size": []}],
    ["bold", "italic", "underline", "strike", "blockquote"],
    [{"list": "ordered"}, {"list": "bullet"}, {"indent": "-1"}, {"indent": "+1"}],
    ["link", "image"],
]

# Get today's date
today = datetime.now()

# Format the date
formatted_date = today.strftime("%Y-%m-%d")

app.layout = html.Div(
    [
        fcc.FullCalendarComponent(
            id="calendar",  # Unique ID for the component
            initialView="listWeek",  # dayGridMonth, timeGridWeek, timeGridDay, listWeek,
            # dayGridWeek, dayGridYear, multiMonthYear, resourceTimeline, resourceTimeGridDay, resourceTimeLineWeek
            headerToolbar={
                "left": "prev,next today",
                "center": "",
                "right": "listWeek,timeGridDay,timeGridWeek,dayGridMonth",
            },  # Calendar header
            initialDate=f"{formatted_date}",  # Start date for calendar
            editable=True,  # Allow events to be edited
            selectable=True,  # Allow dates to be selected
            events=[],
            nowIndicator=True,  # Show current time indicator
            navLinks=True,  # Allow navigation to other dates
        ),
        dmc.MantineProvider(
            theme={"colorScheme": "dark"},
            children=[
                dmc.Modal(
                    id="modal",
                    size="xl",
                    title="Event Details",
                    zIndex=10000,
                    children=[
                        html.Div(id="modal_event_display_context"),
                        dmc.Space(h=20),
                        dmc.Group(
                            [
                                dmc.Button(
                                    "Close",
                                    color="red",
                                    variant="outline",
                                    id="modal-close-button",
                                ),
                            ],
                        ),
                    ],
                )
            ],
        ),
        dmc.MantineProvider(
            theme={"colorScheme": "dark"},
            children=[
                dmc.Modal(
                    id="add_modal",
                    title="New Event",
                    size="xl",
                    children=[
                        dmc.Grid(
                            children=[
                                dmc.GridCol(
                                    html.Div(
                                        dmc.DatePicker(
                                            id="start_date",
                                            label="Start Date",
                                            value=datetime.now().date(),
                                            styles={"width": "100%"},
                                            disabled=True,
                                        ),
                                        style={"width": "100%"},
                                    ),
                                    span=6,
                                ),
                                dmc.GridCol(
                                    html.Div(
                                        dmc.TimeInput(
                                            label="Start Time",
                                            withSeconds=True,
                                            value=datetime.now(),
                                            id="start_time",
                                        ),
                                        style={"width": "100%"},
                                    ),
                                    span=6,
                                ),
                            ],
                            gutter="xl",
                        ),
                        dmc.Grid(
                            children=[
                                dmc.GridCol(
                                    html.Div(
                                        dmc.DatePicker(
                                            id="end_date",
                                            label="End Date",
                                            value=datetime.now().date(),
                                            styles={"width": "100%"},
                                        ),
                                        style={"width": "100%"},
                                    ),
                                    span=6,
                                ),
                                dmc.GridCol(
                                    html.Div(
                                        dmc.TimeInput(
                                            label="End Time",
                                            withSeconds=True,
                                            value=datetime.now(),
                                            id="end_time",
                                        ),
                                        style={"width": "100%"},
                                    ),
                                    span=6,
                                ),
                            ],
                            gutter="xl",
                        ),
                        dmc.Grid(
                            children=[
                                dmc.GridCol(
                                    span=6,
                                    children=[
                                        dmc.TextInput(
                                            label="Event Title:",
                                            style={"width": "100%"},
                                            id="event_name_input",
                                            required=True,
                                        )
                                    ],
                                ),
                                dmc.GridCol(
                                    span=6,
                                    children=[
                                        dmc.Select(
                                            label="Select event color",
                                            placeholder="Select one",
                                            id="event_color_select",
                                            value="ng",
                                            data=[
                                                {
                                                    "value": "bg-gradient-primary",
                                                    "label": "bg-gradient-primary",
                                                },
                                                {
                                                    "value": "bg-gradient-secondary",
                                                    "label": "bg-gradient-secondary",
                                                },
                                                {
                                                    "value": "bg-gradient-success",
                                                    "label": "bg-gradient-success",
                                                },
                                                {
                                                    "value": "bg-gradient-info",
                                                    "label": "bg-gradient-info",
                                                },
                                                {
                                                    "value": "bg-gradient-warning",
                                                    "label": "bg-gradient-warning",
                                                },
                                                {
                                                    "value": "bg-gradient-danger",
                                                    "label": "bg-gradient-danger",
                                                },
                                                {
                                                    "value": "bg-gradient-light",
                                                    "label": "bg-gradient-light",
                                                },
                                                {
                                                    "value": "bg-gradient-dark",
                                                    "label": "bg-gradient-dark",
                                                },
                                                {
                                                    "value": "bg-gradient-white",
                                                    "label": "bg-gradient-white",
                                                },
                                            ],
                                            style={"width": "100%", "marginBottom": 10},
                                            required=True,
                                        )
                                    ],
                                ),
                            ]
                        ),
                        dash_quill.Quill(
                            id="rich_text_input",
                            modules={
                                "toolbar": quill_mods,
                                "clipboard": {
                                    "matchVisual": False,
                                },
                            },
                        ),
                        dmc.Accordion(
                            children=[
                                dmc.AccordionItem(
                                    [
                                        dmc.AccordionControl("Raw HTML"),
                                        dmc.AccordionPanel(
                                            html.Div(
                                                id="rich_text_output",
                                                style={
                                                    "height": "300px",
                                                    "overflowY": "scroll",
                                                },
                                            )
                                        ),
                                    ],
                                    value="raw_html",
                                ),
                            ],
                        ),
                        dmc.Space(h=20),
                        dmc.Group(
                            [
                                dmc.Button(
                                    "Submit",
                                    id="modal_submit_new_event_button",
                                    color="green",
                                ),
                                dmc.Button(
                                    "Close",
                                    color="red",
                                    variant="outline",
                                    id="modal_close_new_event_button",
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ]
)



if __name__ == "__main__":
    app.run_server(debug=True, port=8056)
