# 专属于djangoCelery项目的任务
from celery import Celery
app = Celery('djangoCelery')


@app.task
def test():
    pass
