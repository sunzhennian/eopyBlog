import os
from jinja2 import Environment, FileSystemLoader
import  commands
import  re
import  BeautifulSoup

class eopyBlogRenderOrg(object):
    def __init__(self):
        print 'OrgRender'
    def renderOrgFile(self,fileWithProperties,Jinjaenv,globalConfig):
        template = Jinjaenv.get_template('post.html')
        all_info = dict(globalConfig.items() + fileWithProperties.items())
        TOC_TEXT_CONTEXT=self.getContext(fileWithProperties)
        if TOC_TEXT_CONTEXT[0] !='':
            all_info['TOC_TEXT'] = TOC_TEXT_CONTEXT[0]
        if TOC_TEXT_CONTEXT[1] !='':
            all_info['CONTEXT']=TOC_TEXT_CONTEXT[1]
        file_save_path = os.path.join(globalConfig['project_path'], all_info['HTMLPATH_SAVE'])
        if not os.path.exists(os.path.dirname(file_save_path)):
            os.makedirs(os.path.dirname(file_save_path))
        with open(file_save_path, 'w') as f:
            f.write(template.render(all_info))

    def renderEntry(self,fileWithProperties):
        status, html = commands.getstatusoutput('emacs -Q --script getEntry.el %s' % (fileWithProperties['FILE']))
        fileWithProperties['ENTRY']=html
        return fileWithProperties

    def getContext(self,orgFile):
        status, html = commands.getstatusoutput('emacs -Q --script getContent.el %s'%(orgFile['FILE']))
        soup=BeautifulSoup.BeautifulSoup(html)
        tocID=soup.findAll(id='text-table-of-contents')
        toc=''
        toc_text=''
        if len(tocID)>0:
            toc=str(tocID[0])
            toc_text_ID=soup.findAll(id='text-table-of-contents')
            if len(toc_text_ID)>0:
                toc_text=str(toc_text_ID[0])
        html_without_toc = html.replace(toc, '')
        html_without_toc = html_without_toc.replace('<h2>Table of Contents</h2>', '')
        html_without_toc = html_without_toc.replace(toc_text, '')
        return (toc_text,html_without_toc)
