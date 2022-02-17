import uuid, base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
from django.core.files.base import ContentFile

def generate_code():
    code = str(uuid.uuid4()).replace("-", "").upper()[:12]
    return code

def get_graph():
    # create the bytes buffer
    buffer = BytesIO()
    # create the plot with the use of BytesIO() as a file like object
    plt.savefig(buffer, format="png")
    # set tge cursor at the beginning of the string
    buffer.seek(0)
    # retreive the entire content of the variable
    image_png = buffer.getvalue()
    # encode the image -> this will return the encoded bytes
    graph = base64.b64encode(image_png)
    # get the string from the image by decoding the image
    graph = graph.decode("utf-8")
    # free the memory of the buffer
    buffer.close()
    
    return graph

def get_key(res_by):
    # assign the key
    if res_by == "#1":    
        key = "transaction_id"
    elif res_by == "#2": 
        key = "created"
    return key
    
def get_chart(chart_type, data, results_by, **kwargs):
    # switch the backend -> in matplotlib, the backend is a tool responsible for drawing the plots
    # we need to use the AGG backend -> AGG =  Anti-Grain Geometry -> works good with png files
    plt.switch_backend("AGG")
    # set the size
    fig = plt.figure(figsize=(10, 4))
    key = get_key(results_by)
    d = data.groupby(key, as_index=False)['total_price'].agg('sum')
    if chart_type == "#1":
        sns.barplot(x=key, y='total_price', data=d) 
    elif chart_type == "#2":
        plt.pie(data=d, x="total_price", labels=d[key].values)
    elif chart_type == "#3":
        plt.plot(data[key], d["total_price"], marker="o", linestyle="dashed")
    
    # adjust the size of the chart in response to the fig size
    plt.tight_layout()
    
    chart = get_graph()
    return chart

def get_report_image(data):
    # will return -> data:image/png, followed by the image string
    _ , str_image = data.split(";base64")
    # decode the image
    decoded_img = base64.b64decode(str_image)
    # create the image name
    img_name = str(uuid.uuid4())[:10] + '.png'
    
    data = ContentFile(decoded_img, name=img_name)
    
    return data
