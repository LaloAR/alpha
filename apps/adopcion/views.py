from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.adopcion.models import Persona, Solicitud
from apps.adopcion.forms import PersonaForm, SolicitudForm

# Create your views here.
def index_adopcion(request):
	return HttpResponse("Index de adopción")



class SolicitudList(ListView):
	model = Solicitud
	template_name = 'adopcion/solicitud_list.html'



class SolicitudCreate(CreateView):
	model = Solicitud
	template_name = 'adopcion/solicitud_form.html'
	form_class = SolicitudForm
	second_form_class = PersonaForm
	success_url = reverse_lazy('adopcion:solicitud_listar')

	def get_context_data(self, **kwargs):
		# Recoger el contexto
		context = super(SolicitudCreate, self).get_context_data(**kwargs)
		# Agregando formularios
		if 'form' not in context:
			context['form'] = self.form_class(self.request.GET)
		if 'form2' not in context:
			context['form2'] = self.second_form_class(self.request.GET)
		return context

	# Guardar formularios y relaciones
	def post(self, request, *args, **kwargs):
		self.object = self.get_object

		# Recoger la información ingresada de los 2 formularios
		form = self.form_class(request.POST)
		form2 = self.second_form_class(request.POST)

		if form.is_valid() and form2.is_valid():
			# "commit=False" es para que no lo guarde hasta que guarde el segundo
			solicitud = form.save(commit=False)
			solicitud.persona = form2.save()
			# Guardamos el objeto
			solicitud.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form, form2=form2))



class SolicitudUpdate(UpdateView):
	model = Solicitud
	second_model = Persona
	template_name = 'adopcion/solicitud_form.html'
	form_class = SolicitudForm
	second_form_class = PersonaForm
	success_url = reverse_lazy('adopcion:solicitud_listar')

	# Traer objetos y renderizarlos en los inputs
	def get_context_data(self, **kwargs):
	    context = super(SolicitudUpdate, self).get_context_data(**kwargs)
	    pk = self.kwargs.get('pk', 0)
	    solicitud = self.model.objects.get(id=pk)
	    persona = self.second_model.objects.get(id=solicitud.persona_id)
	    if 'form' not in context:
	    	context['form'] = self.form_class()
	    if 'form2' not in context:
	    	context['form2'] = self.second_form_class(instance=persona)
	    context['id'] = pk
	    return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		id_solicitud = kwargs['pk']
		solicitud = self.model.objects.get(id=id_solicitud)
		persona = self.second_model.objects.get(id=solicitud.persona_id)
		form = self.form_class(request.POST, instance=solicitud)
		form2 = self.second_form_class(request.POST, instance=persona)
		if form.is_valid() and form2.is_valid():
			form.save()
			form2.save()
			return HttpResponseRedirect(self.get_success_url())
		else:
			return HttpResponseRedirect(self.get_success_url())



class SolicitudDelete(DeleteView):
	model = Solicitud
	template_name = 'adopcion/solicitud_delete.html'
	success_url = reverse_lazy('adopcion:solicitud_listar')
