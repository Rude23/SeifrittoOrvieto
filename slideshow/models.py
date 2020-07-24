from django.db import models
from django.core.files.storage import default_storage
from django.shortcuts import reverse
from PIL import Image

# Create your models here.
class Slide(models.Model):

    img=models.ImageField(upload_to='slideshow')

    show=models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        super(Slide, self).save(args, kwargs)

        path=self.img.path
        img=Image.open(path)

        w , h = img.size

        if w/h < 1.91:
            W=int(h*1.91)+1

            new=Image.new('RGB',(W, h), '#191919')
            box=(int((W - w) / 2.), 0)
            new.paste(img, box)

            new.save(path,format=img.format ,quality=100)

        elif w/h > 1.91:
            H=int(w/1.91)+1

            new = Image.new('RGB',(w,H), '#191919' )
            new.paste(img, (0, int((H-h)/2.)))

            new.save(path, format='JPEG', quality=100)

        super(Slide,self).save(args,kwargs)

        return

    def delete(self, using=None, keep_parents=False):

        default_storage.delete(self.img.path)

        super(Slide, self).delete(using,keep_parents)

    def get_change_show_url(self):

        return reverse("home:change_show", kwargs={ 'id': self.id})
