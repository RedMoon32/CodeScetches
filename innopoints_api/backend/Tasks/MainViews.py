from .views import *


class BaseManageView(APIView):
    """
    The base class for ManageViews
        A ManageView is a view which is used to dispatch the requests to the appropriate views
        This is done so that we can use one URL with different methods (GET, PUT, etc)
    """

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'VIEWS_BY_METHOD'):
            raise Exception('VIEWS_BY_METHOD static dictionary variable must be defined on a ManageView class!')
        if request.method in self.VIEWS_BY_METHOD:
            return self.VIEWS_BY_METHOD[request.method].as_view()(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


class MyTasksManageView(BaseManageView):
    VIEWS_BY_METHOD = {
        'GET': CreatedTasks,
        'PATCH': UpdateTask,
        'DELETE': CloseTask,
    }


class TasksManageView(BaseManageView):
    VIEWS_BY_METHOD = {
        'GET': GetAllTasks,
        'POST': CreateTask,
    }


class ApplicationManageView(BaseManageView):
    VIEWS_BY_METHOD = {
        'GET': GetTaskApplications,
        'POST': UpdateApplicationStatus,
    }


class MyApplicationManageView(BaseManageView):
    VIEWS_BY_METHOD = {
        'GET': GetUserApplications,
        'DELETE': CancelApplication,
        'POST': ApplyForTask,
    }
