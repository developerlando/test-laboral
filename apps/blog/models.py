from django.db import models
from django import forms
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel,  MultiFieldPanel
from modelcluster.fields import ParentalManyToManyField
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.shortcuts import render
from graphene.types import Scalar
from wagtail.core.rich_text import expand_db_html


class RichTextFieldType(Scalar):
    """Serialises RichText content into fully baked HTML
    see https://github.com/wagtail/wagtail/issues/2695#issuecomment-373002412 """
    
    @staticmethod
    def serialize(value):
        return expand_db_html(value)

class Categoria(models.Model):
    """Categorias for a snippet."""
    name = models.CharField(max_length=250)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text='Un tag para identificar articulos',
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Categorias"
        verbose_name_plural = "Categorias del Blog"
        ordering = ["name"]

    def __str__(self):
        return self.name
    
register_snippet(Categoria)

class ArticulosPage(RoutablePageMixin, Page):

    @property
    def get_child_pages(self):
        return self.get_children().public().live()

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        all_posts = ArticuloPage.objects.live().public().order_by('-first_published_at')
        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            all_posts = all_posts.filter(tags__slug__in=[tags])
        # Paginate all posts by 2 per page
        paginator = Paginator(all_posts, 2)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context["posts"] = ArticuloPage.objects.live().public()
        context["posts"] = posts
        context["categorias"] = Categoria.objects.all()
        return context
   
    @route(r'^latest/$', name="latest_posts")
    def latest_blog_posts_only_shows_last_5(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        
        context["posts"] = context["posts"][:1]
        return render(request, "blog/latest_posts.html", context)
    
    @route(r"^category/(?P<cat_slug>[-\w]*)/$", name="category_view")
    def category_view(self, request, cat_slug):
        """Find blog posts based on a category."""
        context = self.get_context(request)
        try:
            # Look for the blog category by its slug.
            categorias = Categoria.objects.get(slug=cat_slug)
        except Exception:
            # Blog categorias doesnt exist (ie /blog/categorias/missing-categorias/)
            # Redirect to self.url, return a 404.. that's up to you!
            categorias = None

        if categorias is None:
            # This is an additional check.
            # If the categorias is None, do something. Maybe default to a particular categorias.
            # Or redirect the user to /blog/ ¯\_(ツ)_/¯
            pass
        context["posts"] = ArticuloPage.objects.live().public().filter(categories__in=[categorias])

        # Note: The below template (latest_posts.html) will need to be adjusted
        return render(request, "blog/articulo_page.html", context)

   
    def get_sitemap_urls(self, request):
        # Uncomment to have no sitemap for this page
        # return []
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            {
                "location": self.full_url + self.reverse_subpage("latest_posts"),
                "lastmod": (self.last_published_at or self.latest_revision_created_at),
                "priority": 0.9,
            }
        )
        return sitemap

    subpage_types = ["ArticuloPage"]


class ArticuloPage(Page):
    """Pagina Indivual"""
    contenido = RichTextField(
        blank=True,
        null=False,
        help_text="contenido del articulo"
        )
    
    imagen = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True, 
        related_name='portada',
        on_delete=models.SET_NULL,
        )
    
    categorias = ParentalManyToManyField(
        Categoria, 
        blank=False

        )

    content_panels = Page.content_panels + [
        FieldPanel("contenido", classname="full"),
        FieldPanel("imagen", classname="full"),
        MultiFieldPanel(
            [
                FieldPanel("categorias", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Categorias"
        ),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('tittle'),
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        context["categorias"] = Categoria.objects.all()
        return context

    parent_page_types = ["ArticulosPage"]

    
