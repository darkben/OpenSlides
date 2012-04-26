#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    openslides.projector.urls
    ~~~~~~~~~~~~~~~~~~~~~~~~

    URL list for the projector app.

    :copyright: 2011, 2012 by OpenSlides team, see AUTHORS.
    :license: GNU GPL, see LICENSE for more details.
"""

from django.conf.urls.defaults import *

from utils.views import CreateView

from views import ControlView, ActivateView
from agenda.views import ItemUpdate
from models import ProjectorSlide


urlpatterns = patterns('projector.views',
    url(r'^$', 'active_slide',
        {'sid': None},
        name='projector_show',
    ),

    url(r'^preview/(?P<sid>[^/]*)/$',
        'active_slide',
        name='projctor_preview_slide',
    ),

    url(r'^control/$',
        ControlView.as_view(),
        name='projector_control',
    ),

    url(r'^activate/(?P<sid>[^/]*)/$',
        ActivateView.as_view(),
        name='projector_activate_slide',
    ),

    url(r'^activate/(?P<sid>[^/]*)/summary/$',
        ActivateView.as_view(),
        {'summary': True},
        name='projector_activate_summary',
    ),

    url(r'^new/$',
        CreateView.as_view(
            success_url='projector_control',
            model=ProjectorSlide,
            template_name='projector/new.html',
            permission_required='projector.can_manage_projector'
        ),
        name='custom_slides_new',
    ),

    url(r'^bigger/$', 'projector_edit', {'direction': 'bigger'},
        name='projector_bigger'),

    url(r'^smaller/$', 'projector_edit', {'direction': 'smaller'},
        name='projector_smaller'),

    url(r'^up/$', 'projector_edit', {'direction': 'up'},
        name='projector_up'),

    url(r'^down/$', 'projector_edit', {'direction': 'down'},
        name='projector_down'),

    url(r'^clean/$', 'projector_edit', {'direction': 'clean'},
        name='projector_clean'),

    url(r'^countdown/show/$', 'projector_countdown', {'command': 'show'},
        name='countdown_open'),

    url(r'^countdown/hide/$', 'projector_countdown', {'command': 'hide'},
        name='countdown_close'),

    url(r'^countdown/reset/$', 'projector_countdown', {'command': 'reset'},
        name='countdown_reset'),

    url(r'^countdown/start/$', 'projector_countdown', {'command': 'start'},
        name='countdown_start'),

    url(r'^countdown/stop/$', 'projector_countdown', {'command': 'stop'},
        name='countdown_stop'),

    url(r'^countdown/set-default/$', 'projector_countdown', {'command': 'set_default'},
        name='countdown_set_default'),
)
