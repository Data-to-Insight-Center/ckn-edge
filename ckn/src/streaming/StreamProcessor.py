import faust

app = faust.App(
    'page_views_2',
    broker='kafka://localhost:9092',
    partitions=1,
)

class PageView(faust.Record):
    id: str
    user: str


INPUT_TOPIC = "test-input2"
OUTPUT_TOPIC = "test-output"
BROKERS = 'kafka://localhost:9092'

page_view_topic = app.topic('page_views_2', value_type=PageView)
page_views = app.Table('page_views_2', default=int)


@app.agent(page_view_topic)
async def count_page_views(views):
    await page_view_topic.declare()
    async for view in views.group_by(PageView.id):
        page_views[view.id] += 1
        print("here")

if __name__ == '__main__':
    app.main()