from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question, NameModel
from .models import NameForm
from .FSM import WorkFlowFSM
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class NameModelView(generic.ListView):
    template_name = 'polls/flowindex.html'
    context_object_name = 'latest_namemodel_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return NameModel.objects.order_by('id')[:]

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def excute_trans_action(model_instance, after_trans_action):
    if 'assign_to' in after_trans_action:
        for field in model_instance._meta.get_fields():
            if field.verbose_name == after_trans_action['assign_to']:
                attr_value = getattr(model_instance, field.name)
        model_instance.assigned_to = attr_value

def myflowdetail(request,model_id):
    workflowfsm = WorkFlowFSM()
    if request.method == 'POST':
        model_instance = NameModel.objects.get(pk=model_id)
        form_instance = NameForm(request.POST, instance=model_instance)
        #Done:Add code for state trans here
        form_instance.save()
        trigger = request.POST['trigger']

        #TODO:Add code for excute after_trans_action
        after_trans_action = workflowfsm.FSM_get_trans_action(model_instance.curent_state, trigger)
        excute_trans_action(model_instance, after_trans_action)

        model_instance.curent_state = workflowfsm.FSM_get_triger_and_desstate(model_instance.curent_state)[trigger]
        model_instance.save()
        return HttpResponseRedirect(reverse('polls:myflowindex'))
    else:
        namemodel = get_object_or_404(NameModel, pk=model_id)
        form = NameForm(instance=namemodel)
        form.fields['curent_state'].widget.attrs['readonly'] = True
        #Done:Add code for state trans here
        triggerlist = workflowfsm.FSM_get_trigger(namemodel.curent_state)
        return render(request, 'polls/flowdetail.html', {'form':form, 'model_id':model_id,'trigger':triggerlist})

def myflow(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #TODO:check model field and database colum
            form.save()
            #return HttpResponse("Hello, world. Thanks for submit.")
            return HttpResponseRedirect(reverse('polls:myflowindex'))

    # if a GET (or any other method) we'll create a blank form
    else:
        workflowfsm = WorkFlowFSM()
        init_state = workflowfsm.FSM_get_init_state() #FSM.FSM_get_init_state()
        form = NameForm(initial={'curent_state': init_state})
    return render(request, 'polls/name.html', {'form':form})

def myflowprocess(request):
    return HttpResponse("Hello, world. This is form processing result.")
