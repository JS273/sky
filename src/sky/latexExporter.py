import os, re

from toolbox.translationRules import translation_rules, si_rules

def check_translation_rules(string, start, stop, use_si=False):
    adjusted_string = string[:]
    cont = string[start:stop]
    cont = [rule[1] for gg, rule in enumerate(translation_rules) if cont == rule[0]]
    if cont:
        if use_si:
            cont_si = [cont[0].replace(rule[0], rule[1]) for gg, rule in enumerate(si_rules) if rule[0] in cont[0]]
            if cont_si:
                cont = cont_si
        adjusted_string = string[:start] + cont[0] + string[stop:]
    return adjusted_string

def latex_graphic_export(figure,
                         graphic_name='LatexFigure',
                         file_path=os.getcwd(),
                         ink_dir=r'C:\Program Files\Inkscape\bin',
                         pdf_tex_dir=r'./pics/',
                         size=(6.3, 2.7),
                         stay_tex=False,
                         insert_hints=False,
                         use_replacing_rules=False,
                         use_si_pack=False,
                         git_path='',
                         git_push=False):

    """ Matplotlib/Inkscape Latex Export S.Rothe / S.Hoffmann use_replacing_rules

    This function allows you to export a Matplotlib figure using Inkscape. The image is split by
    Inkscape into a PDF and a PDF_TEX file and can later be embedded in Latex with matching font sizes and styles.

        figure = fig,                                --> matplotlib figure
        graphic_name = 'LatexFigure',                --> Name of the file
        file_path = r'C:\Klaus\Dieter_s\pictures',   --> Where should it be saved (eg. path of your thesis)
        ink_dir = r'C:\Program Files\Inkscape\bin',  --> path where Inkscape is Installed (inkscape.exe)
        pdf_tex_dir = r'./pictures/')                --> name of your picture directory in Latex structure
        stay_tex                                     --> the tx file stays and the pdf will be changed
    """
    if git_push:
        os.chdir(file_path)
        os.system(fr'cmd /c git pull')

    # ============== Check file path and safe the main pdf to convert later ============================================
    if len(file_path) == 0 or file_path[0] in ['.', ' ']:
        file_path = os.path.join(os.getcwd())
    pdf_file = os.path.join(file_path, graphic_name)
    for fm in [pdf_file, pdf_file+'Control']:
        figure.savefig(fr'{fm}.pdf',
                       bbox_inches='tight',
                       pad_inches=0.0,
                       transparent=True)

    # ============== Existing data with the same name will be removed ==================================================
    if os.path.exists(fr'{pdf_file}.pdf_tex'):
        os.remove(fr'{pdf_file}.pdf_tex')

    # ============== Try command for Inkscape < 1.0 ====================================================================
    os.chdir(ink_dir)
    command = f'.\inkscape {pdf_file}.pdf --export-pdf={pdf_file}.pdf --export-latex'
    os.system(fr'cmd /c {command}')

    # ============== If no pdf_tex file was created, try command for Inkscape >= 1.0 ===================================
    if os.path.exists(fr'{pdf_file}.pdf_tex') is False:
        command = f'.\inkscape {pdf_file}.pdf --export-filename={pdf_file}.pdf --export-latex'
        os.system(fr'cmd /c {command}')

    # ============== Read in the pdf_tex file and store contents into new variable =====================================
    os.chdir(file_path)
    file = open('{}.pdf_tex'.format(graphic_name), 'r')
    contents = file.readlines()
    file.close()

    # ============== Change the relevant paths in the pdf_tex file =====================================================
    if insert_hints is False:
        contents = contents[26:]

    pdf_including = []
    tex_including = []
    num_including = []
    idx_including = []

    idx_start_insert = 0
    for ii, content in enumerate(contents):
        check = re.search(r'put', content)
        if check is not None:
            if idx_start_insert == 0:
                idx_start_insert = ii
            check = re.search(fr'{graphic_name}.pdf', content)
            if check is not None:
                value = check.string[0:check.start()] + f'{pdf_tex_dir}{graphic_name}.pdf' + check.string[check.end():]
                pdf_including.append(value)
                contents[ii] = value
            else:
                start = content.index('{l}') + 3
                stop = content.index(r'\end')
                if content[start:stop].replace(".", "", 1).isdigit():
                    num_including.append(content)
                else:
                    if use_replacing_rules:
                        # if any(x in content[start:stop] for x in ["\\", r"_"]):
                        #     content = content[:start] + "$" + content[start:stop] + "$" + content[stop:]
                        content = check_translation_rules(string=content, start=start, stop=stop, use_si=use_si_pack)
                    tex_including.append(content)
            idx_including.append(ii)

    for idx, content in zip(idx_including,
                            pdf_including + sorted(num_including, key=len) + sorted(tex_including, key=len)):
        contents[idx] = content

    # ============== Save a new pdf_tex file ===========================================================================
    if stay_tex is False:
        file = open('{}.tex'.format(graphic_name), 'w')
        contents = "".join(contents)
        file.write(contents)
        file.close()

    if os.path.exists(fr'{pdf_file}.pdf_tex'):
        os.remove(fr'{pdf_file}.pdf_tex')

    if os.path.exists(git_path):
        os.chdir(git_path)
        if git_push:
            comment = f'"Change the figure: {graphic_name}"'
            commands = [r"git add --all",
                        r"git commit -a -m " + comment,
                        r"git push"]
            for cmd in commands:
                os.system(fr'cmd /c {cmd}')

