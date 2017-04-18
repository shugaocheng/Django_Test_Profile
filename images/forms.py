from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title','url','description')
        # HiddenInput控件,在HTML页面被渲染成属性<type="hidden">
        # 该控件用户无法看见
        widgets = {
            'url':forms.HiddenInput,
        }

    # 检查url
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg','jpeg']
        # rsplit从右边第一个'.'分界,例:'sdasdas.jpg'>>['sdasdas','jpg']
        extension = url.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('当前URL不能匹配有效的图片拓展名称')
        return url

    def save(self,force_insert=False,
             force_update=False,
             commit=True):
        image = super(ImageCreateForm,self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title),image_url.rsplit('.',1)[1].lower())
        response = request.urlopen(image_url)
        # 调用save()方法把图片传给ContentFiel对象,该对象被下载的文件实例化
        # 这样就可以将文件保存到项目中的media路径下,传递参数commit=False来避免对象被保存到数据库
        # ContentFile继承自file类,保存文件
        image.image.save(image_name,
                         ContentFile(response.read()),
                         save=False)
        if commit:
            image.save()
        return image
