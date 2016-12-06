import os
import re

class FileSystemProcessing(object):
    def __init__(self,dir):
        self.dir=dir

    def GetAllFilesSortedByDate(self,ext=None):
        allFiles = self.GetFileFromThisRootDir(self.dir,ext)
        filesWithProperties = []
        for file in allFiles:
            properties = self.getFileProperties(file)
            filesWithProperties.append(properties)
        filesWithProperties.sort(key=lambda date: date.get('DATE'), reverse=True)
        filesWithProperties = self.AddAddtionalInfos(filesWithProperties)
        return filesWithProperties

    def GetFileFromThisRootDir(self, dir, ext=None):
        allfiles = []
        needExtFilter = (ext != None)
        for root, dirs, files in os.walk(dir):
            for filespath in files:
                filepath = os.path.join(root, filespath)
                extension = os.path.splitext(filepath)[1][1:]
                if needExtFilter and extension in ext:
                    allfiles.append(filepath)
                elif not needExtFilter:
                    allfiles.append(filepath)
        return allfiles

    def getFileProperties(self,file):
        ## Return a tuple in format('TITLE','DATE','OPTIONS')
        ## output_file_format YYYY-MM-DD
        ## pubdir
        pub_dir = r'publish'
        keywords = ['TITLE', 'DATE']
        f = open(file, 'r')
        lines = f.readlines()
        result_keyword = {}
        result_keyword['FILE'] = file
        for line_index in range(0, 10):
            line = lines[line_index]
            line = line.strip()
            if line.startswith('#'):
                for keyword_index in range(0, len(keywords)):
                    keyword = keywords[keyword_index]
                    if line.startswith("#+" + keyword):
                        if keyword == 'DATE':
                            result_keyword[keyword] = re.findall(r"\d{1,4}-\d{1,3}-\d{1,3}", line)[0]
                        else:
                            result_keyword[keyword] = line.replace('#+' + keyword + ':', '')
        result_keyword['HTMLPATH_SAVE'] = os.path.join(pub_dir, 'post', result_keyword['DATE'].replace('-', '/'),
                                                       os.path.splitext(os.path.split(file)[-1])[0] + '.html')
        result_keyword['HTML_URL'] = os.path.join('/post', result_keyword['DATE'].replace('-', '/'),
                                                  os.path.splitext(os.path.split(file)[-1])[0] + '.html')
        return result_keyword

    def AddAddtionalInfos(self,postListSorted):
        for file_idx in range(0, len(postListSorted)):
            if file_idx == 0 and len(postListSorted)>1:
                postListSorted[file_idx]['NEXT_POST'] = postListSorted[file_idx + 1]['HTML_URL']
            elif file_idx == len(postListSorted) - 1 and len(postListSorted)>1:
                postListSorted[file_idx]['PREVIOUS_POST'] = postListSorted[file_idx - 1]['HTML_URL']
            elif len(postListSorted)>1:
                postListSorted[file_idx]['PREVIOUS_POST'] = postListSorted[file_idx - 1]['HTML_URL']
                postListSorted[file_idx]['NEXT_POST'] = postListSorted[file_idx + 1]['HTML_URL']
        return postListSorted