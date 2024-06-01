import streamlit as st
import leafmap.foliumap as leafmap
from keras.models import load_model
from PIL import Image
import numpy as np
from util import classify, set_background


st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
Web App URL: <https://capstoneproject37.streamlit.app/>
GitHub Repository: <https://github.com/TaufiiquRahman/CapstoneProject37>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/JFyI8Fl.jpeg"
st.sidebar.image(logo)

# Customize page title
st.title("Streamlit for Quality Control Casting Production")

st.markdown(
    """
    This multipage app template demonstrates various interactive web apps created using [streamlit](https://streamlit.io) and [leafmap](https://leafmap.org). It is an open-source project and you are very welcome to contribute to the [GitHub repository](https://github.com/giswqs/streamlit-multipage-template).
    """
)

st.header('Please upload a Casting Product Image')

file = st.file_uploader('', type=['jpeg', 'jpg', 'png'])

model = load_model('./modelcast.h5')

with open('./model/label.txt', 'r') as f:
    class_names = [a[:-1].split(' ')[1] for a in f.readlines()]
    f.close()


# display image
if file is not None:
    image = Image.open(file).convert('RGB')
    st.image(image, use_column_width=True)

    # classify image
    class_name, conf_score = classify(image, model, class_names)

    # write classification
    st.write("## {}".format(class_name))
    st.write("### score: {}%".format(int(conf_score * 1000) / 10))

markdown = """
1. For the [GitHub repository](https://github.com/giswqs/streamlit-multipage-template) or [use it as a template](https://github.com/giswqs/streamlit-multipage-template/generate) for your own project.
2. Customize the sidebar by changing the sidebar text and logo in each Python files.
3. Find your favorite emoji from https://emojipedia.org.
4. Add a new app to the `pages/` directory with an emoji in the file name, e.g., `1_🚀_Chart.py`.

"""

st.markdown(markdown)

m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
