from data_processing_dash import clean_time, categorize_time
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def byYearGraph(df): 
    if df.empty:
        return px.line()  # Return empty figure if DataFrame is empty
    fig = px.line(df, x='Year', y='Attacks', title='Shark Attack by Year')  # a line
    fig.update_layout(
                        yaxis_title='Attacks',
                        plot_bgcolor='rgba(252,248,244,1.00)',
                        paper_bgcolor='cornsilk',
                        font=dict(
                            family="Montserrat",
                            size=18,
                            color='black'
                        )
                    )
    fig.update_traces(
        line_color='rgb(102,197,204)',
        hovertemplate='Year: %{x}<br>Number: %{y}'
    )
    return fig


def byActivityGraph(df):
    if df.empty:
        return px.bar()  # Return empty figure if DataFrame is empty
    prov_activity = df[df.Type == 'Provoked'].groupby('Activity')['Activity'].count().sort_values(ascending=False)[:10]
    fig = px.bar(prov_activity, x=prov_activity.values, y=prov_activity.index, orientation='h', labels={'index':'','x':'Attack Count'},
                title='Provoked Attacks by Activity')  # barplot
    fig.update_layout(
                        plot_bgcolor='rgba(252,248,244,1.00)',
                        paper_bgcolor='cornsilk',
                        font=dict(
                            family="Montserrat",
                            size=18,
                            color='black'
                        )
                    )
    fig.update_traces(marker_color='rgb(102, 197, 204)')  # bar colors
    return fig


def bySexGraph(df):
    if df.empty:
        return px.pie()  # Return empty figure if DataFrame is empty
    bySex_count = df['Sex'].value_counts().reset_index().rename(columns={'index': 'Gender', 'Sex': 'Count'})
    fig = px.pie(data_frame=bySex_count,
                 values='Count',
                 names='Gender',
                 title='Shark Attack by Gender',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(textposition='outside', textinfo='label+percent')
    fig.update_layout(paper_bgcolor='cornsilk',
                     legend_title='Gender',
                     font=dict(
                         family="Montserrat",
                         size=18,
                         color='black'
                     ))
    return fig


def hoursGraph(df):
    if df.empty:
        return px.histogram()  # Return empty figure if DataFrame is empty
    shark_n = df.copy()
    shark_n.dropna(subset=['Time'], inplace=True)
    time_periods = ["evening", "morning", "night", "afternoon"]
    shark_n['Time'] = shark_n['Time'].apply(clean_time)
    shark_n['Time'] = shark_n['Time'].str.replace(r'^(.*?)(\d{2})$', r'\2', regex=True)
    shark_n = shark_n[shark_n['Time'].isin(time_periods) | (shark_n['Time'].str.isdigit())]
    numeric_time_values = shark_n[shark_n['Time'].str.isdigit()]['Time'].astype(int)
    numeric_time_values = numeric_time_values[numeric_time_values <= 24]
    fig = px.histogram(numeric_time_values, x="Time", title="Hour of the attack")
    fig.update_xaxes(title_text="Time (hours)")
    fig.update_yaxes(title_text="Number of attacks")
    fig.update_traces(marker_color="rgb(102, 197, 204)", marker_line_color="black", marker_line_width=1, opacity=1)
    fig.update_layout(plot_bgcolor='rgba(252,248,244,1.00)',
                      paper_bgcolor='cornsilk',
                      barmode="overlay",
                      bargap=0.1,
                      font=dict(
                          family="Montserrat",
                          size=18,
                          color='black'
                      ))
    return fig


def periodGraph(df):
    if df.empty:
        return px.pie()  # Return empty figure if DataFrame is empty
    shark_n = df.copy()
    shark_n.dropna(subset=['Time'], inplace=True)
    time_periods = ["evening", "morning", "night", "afternoon"]
    shark_n['Time'] = shark_n['Time'].apply(clean_time)
    shark_n['Time'] = shark_n['Time'].str.replace(r'^(.*?)(\d{2})$', r'\2', regex=True)
    shark_n = shark_n[shark_n['Time'].isin(time_periods) | (shark_n['Time'].str.isdigit())]
    shark_f = shark_n.copy()
    shark_f['Time'] = shark_f['Time'].apply(categorize_time)
    time_count = shark_f['Time'].value_counts().reset_index().rename(columns={'index': 'Time', 'Time': 'Count'})
    fig = px.pie(data_frame=time_count,
                 values='Count',
                 names='Time',
                 title='Time of the attack',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(textposition='outside', textinfo='label+percent')
    fig.update_layout(paper_bgcolor='cornsilk',
                     legend_title='Time',
                     font=dict(
                         family="Montserrat",
                         size=18,
                         color='black'
                     ))
    return fig


def ageGraph(df):
    if df.empty:
        return px.histogram()  # Return empty figure if DataFrame is empty
    shark_a = df.copy()
    shark_a.dropna(subset=['Age'], inplace=True)
    shark_a = shark_a[shark_a['Age'].str.match(r'^\d+(\.\d+)?$')]
    shark_a['Fatal (Y/N)'] = shark_a['Fatal (Y/N)'].str.upper()
    shark_a = shark_a[shark_a['Fatal (Y/N)'].isin(['Y', 'N', 'UNKNOWN'])]
    shark_a['Age'] = pd.to_numeric(shark_a['Age'], errors='coerce')
    shark_sorted = shark_a.sort_values(by='Age', ascending=True)
    fig = px.histogram(shark_sorted, x="Age", color="Fatal (Y/N)", title="Age and lethality")
    fig.update_xaxes(title_text="Age")
    fig.update_yaxes(title_text="Number of attacks") 
    fig.update_layout(
        plot_bgcolor='rgba(252,248,244,1.00)',
        paper_bgcolor='cornsilk',
        legend_title='Fatal',
        font=dict(
            family="Montserrat",
            size=18,
            color='black'
        ),
        legend=dict(
            font=dict(size=14)
        )
    )
    fig.update_traces(
        selector=dict(name='Y'),
        name='YES'
    )
    fig.update_traces(
        selector=dict(name='N'),
        name='NO'
    )
    return fig, shark_sorted

# Fonction pour comparer les attaques fatales et non fatales par espèce
def fatalandnot(sharks_species):

            filtered_df_Y = sharks_species[sharks_species['Fatal (Y/N)'] == 'Y']#we make a graph according to the value selected
            species_attack_Y = filtered_df_Y.groupby('Species')['Species'].count().sort_values(ascending=False)[1:15]

            filtered_df_N = sharks_species[sharks_species['Fatal (Y/N)'] == 'Y']#we make a graph according to the value selected
            species_attack_N = filtered_df_Y.groupby('Species')['Species'].count().sort_values(ascending=False)[1:15]

            dataY = go.Bar(x = species_attack_Y.index,y=species_attack_Y.values,text=species_attack_Y.values,textposition='auto', marker_color='rgb(102,197,204)')
            dataN= go.Bar(x = species_attack_N.index,y=species_attack_N.values,text=species_attack_N.values,textposition='auto', marker_color='rgb(102,197,204)')

            layout = go.Layout( 
                        xaxis=dict(title='Species'),
                        yaxis=dict(title='Attack Count',visible=False),
                        paper_bgcolor='cornsilk',
                        plot_bgcolor='rgba(252,248,244,1.00)',
                        font = dict(
                            family = "Montserrat",
                            size = 18,
                            color = 'black'
                            )
                        )

            fig1 = go.Figure(
                data=dataY,
                layout=layout
            )   

            fig2 = go.Figure(
                data=dataN,
                layout=layout
            )   

            return fig1, fig2