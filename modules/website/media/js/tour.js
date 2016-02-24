$(function(){
    window.tour = new Tour({
        onShow: function() {
            $('#overlay').show();
        },
        onEnd: function() {
            $('#overlay').hide();
        }
    });

    $('.play-tour').on('click', function(e) {
        if (typeof(window.tour) != "undefined"){
            window.tour.restart();
        }
    });

    tour.addStep({
        path: "/events/",
        element: ".container table",
        title: gettext("Latest errors"),
        content: gettext("You can see all important informations in on single view, so you can react quickly."),
        placement: 'top'
    });

    tour.addStep({
        path: "/events/",
        element: "#chart",
        title: gettext("Graphing view"),
        content: gettext("Errors are also agreggated to graphing view. So you can observe events trends."),
        placement: 'bottom'
    });

    tour.addStep({
        path: "/events/",
        element: "#traffic",
        title: gettext("Quota system"),
        content: gettext("Here you have an overview of available credits, to get more please upgrade your account."),
        placement: 'bottom'
    });

    tour.addStep({
        path: "/bundles/",
        element: ".navbar .nav:nth-child(1) > li.active",
        title: gettext("Bundles of javascript"),
        content: gettext("Bundles are collections of resource (javascript) files, which are targerted to specific website domain."),
        placement: 'bottom'
    });

    tour.addStep({
        path: "/api/doc/",
        element: ".navbar .nav:nth-child(1) > li.active",
        title: gettext("Site integration"),
        content: gettext("To enable error tracking of processed files please paste errorify snippet into your pages, which is extremely small and loaded asynchronous."),
        placement: 'bottom'
    });

    tour.addStep({
        path: "/api/",
        element: "#.navbar .nav:nth-child(1) > li.active",
        title: gettext("Api development"),
        content: gettext("Automate the process using our APIs and never relay on third-party proxy services. All features all available through programmable API. See examples bellow."),
        placement: 'bottom'
    });

    tour.addStep({
        path: "/auth/profile/",
        element: "#id_timezone_chzn",
        title: gettext("Your timezone"),
        content: gettext("Don't forget to set your correct timezone, so we can tell you what time errors happen at by your timezone."),
        placement: 'top'
    });

    tour.addStep({
        path: "/bundles/",
        element: ".page-header a.action:nth-child(3)",
        title: gettext("Create bundle"),
        content: gettext("Start using the app now, by creating new bundle. Please use contact form for any questions or comments (located at bottom of the page)."),
        placement: 'bottom'
    })

    tour.start();
});
