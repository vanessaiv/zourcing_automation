from parser_custom import resume_parser
import os
os.chdir('C:\\Users\Lenovo\Google Drive (vanessa.cruz@quantumworks.io)\@zourcing')
cvs = ['1107 (Jose Luis Rodriguez Hernandez)\Cvs 26 marzo\CVAndreaMonserratMartinezMurillo.pdf',
        '1512(Flor de María Amado Ruiz)\ABRAAM BONILLA.pdf', '1211 (Marisol Rojas)\\4 Marzo\Angelica LM CV2020.pdf',
        '1431 (Roberto Puon)\CVs 19 marzo\CV Alducin Garcia Marco Antonio 2020.pdf', '1438 (Edith Pantaleon Gutierrez)\CV Juan Antonio.pdf',
        '1089 (Luz Vistraín)\Daniel_Pedraza.pdf', '1089 (Luz Vistraín)\Carlos Alberto Torres Martinez Embebidos.pdf', '1089 (Luz Vistraín)\Joel Baez.pdf',
        '1089 (Luz Vistraín)\Technical Lead  Oscar Valencia.pdf', '1511\CV VICTOR GARCIA.docx', '1438 (Edith Pantaleon Gutierrez)\CVVMSR.docx',
        '1348 (Karla Muciño)\Gerentes Admon y Finanzas\CVGeorginaOrtegaOsorio.docx', '1305 (Daniela Uribe)\Curriculum Jocelyn.docx',
        '1089 (Luz Vistraín)\Carlos Alberto Torres Martinez Embebidos.docx', '1089 (Luz Vistraín)\\6 de Abril\SAP ABAP Arturo Castillo.pdf',
        '1511/CV Alberto Cardenas.pdf']

cv_path = './CVS/'

CVs = [cv_path + cv for cv in cvs]


resume_parser.resume_result_wrapper(CVs[1])
resume_parser.resume_result_wrapper(CVs[11])
resume_parser.resume_result_wrapper(CVs[12])

resume_parser.resume_result_wrapper(CVs[5])
resume_parser.resume_result_wrapper(CVs[6])
