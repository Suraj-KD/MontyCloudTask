from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.views import APIView
from MyLogs.models import MyLogs
from rest_framework.response import Response


# Create your views here.
class GetLogs(APIView):

    def dispatch(self, request, *args, **kwargs):
        self.context_dict = {'head': {}, 'body': {}}

    def post(self, request):
        data = request.data
        context = self.getLogs(data)
        return Response(data=context)

    def getLogs(self, data):
        server_name = data.get('server_name')
        if not server_name:
            self.context_dict['status'] = "1"
            self.context_dict['statusDescription'] = "Server name not provided in input"
            return self.context_dict

        log = MyLogs.objects.filter(server=server_name).first()
        if not log:
            self.context_dict['status'] = "1"
            self.context_dict['statusDescription'] = "No log found with name={}".format(server_name)
            return self.context_dict

        context_dict = {'Server Name': log.server,
                        'Creation Date': log.logging_date,
                        'Logging Level': log.logging_mode,
                        'Logged Data': log.logged_data}
        return context_dict


class AddLog(APIView):
    def dispatch(self, request, *args, **kwargs):
        self.contex_dict = {'head': {}, 'body': {}}

    def post(self, request):
        data = request.data
        context = self.addLog(data)
        return Response(data=context)

    def addLog(self, data):
        try:
            server_name = data.get('server_name')
            logging_mode = data.get('logging_level')
            if not server_name:
                self.contex_dict['head']['status'] = "1"
                self.contex_dict['head']['statusDescription'] = "Server name not provided in input"
            else:
                log = MyLogs.objects.create(server=server_name, logging_mode=logging_mode,
                                            logged_data=data.get('logged_data'))
                self.contex_dict['body']["Server Name"] = log.server
                self.contex_dict['body']["Logging Date"] = log.logging_date
                self.contex_dict['body']["Logging Level"] = log.logging_mode
                self.contex_dict['body']["Logged Data"] = log.logged_data
                self.contex_dict['head']['status'] = "0"
                self.contex_dict['head']['statusDescription'] = "Success"

        except IntegrityError:
            self.contex_dict['head']['status'] = "1"
            self.contex_dict['statusDescription'] = "Duplicate entry not allowed"

        except Exception as e:
            self.contex_dict['head']['status'] = "1"
            self.contex_dict['statusDescription'] = 'Failed with error {}'.format(e)

        return self.context_dict
