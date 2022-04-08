from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render
import time

# Create your views here.
from datetime import datetime


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def report_generator(request):
    if request.method == 'POST':
        physician_name = request.POST.get('physician_name')
        physician_contact = request.POST.get('physician_contact')
        patient_f_name = request.POST.get('patient_f_name')
        patient_l_name = request.POST.get('patient_l_name')
        dob = request.POST.get('dob')
        patient_contact = request.POST.get('patient_contact')
        complaint = request.POST.get('complaint')
        consultation_note = request.POST.get('consultation_note')
        ip = get_client_ip(request)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        data = {
            "physician_name": physician_name,
            "physician_contact": physician_contact,
            "patient_f_name": patient_f_name,
            "patient_l_name": patient_l_name,
            "dob": dob,
            "patient_contact": patient_contact,
            "complaint": complaint,
            "consultation_note": consultation_note,
            "time": current_time,
            "ip": ip,
        }

        pdf = render_to_pdf('pdf_template.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"CR_{patient_l_name}_{patient_f_name}_{dob}.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    else:
        return render(request, 'index.html')
