import yaml
import os
import eopyBlog.eopyBlogUtil
import eopyBlog_render_org.eopyBlogRenderOrg
from jinja2 import Environment, FileSystemLoader
import sys
#print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')
import  commands

if __name__== "__main__":
    project_path=r'/home/sunzn/PycharmProjects/eopyBlog'
    f = open(os.path.join(project_path,'_config.yml'))
    config = yaml.load(f)
    config['project_path'] =project_path
    file_sys_processing=eopyBlog.eopyBlogUtil.FileSystemProcessing(os.path.join(project_path,config['source_dir']))
    FilesSortedByDate=file_sys_processing.GetAllFilesSortedByDate('org')
    env = Environment(loader=FileSystemLoader(os.path.join(project_path,'themes',config['theme'],'template')))
    orgRender=eopyBlog_render_org.eopyBlogRenderOrg.eopyBlogRenderOrg()
    for file in FilesSortedByDate:
        file=orgRender.renderEntry(file)

    Index={}
    Index['POSTs']=FilesSortedByDate
    template = env.get_template('index.html')
    with open(os.path.join(project_path,config['public_dir'],'index.html'), 'w') as f:
        f.write(template.render(Index))
    for file in FilesSortedByDate:
        orgRender.renderOrgFile(file,env,config)
