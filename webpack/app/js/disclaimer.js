export default class Disclaimer {
  constructor() {
    // $('#portal-searchbox .searchField').on('focus', (e) => {
    //   e.preventDefault();
    //   if ($('#search-overlay').length === 0) {
    //     $('#portal-searchbox > form').append('<div id="search-overlay"></div>');
    //   }
    //   $('#search-overlay').show();
    //   $('#portal-searchbox .search-suggestions').css('display', 'block');
    // });

    // $(document).on('click', '#search-overlay',  (e) => {
    //   e.preventDefault();
    //   $('#search-overlay').hide();
    //   $('#portal-searchbox .search-suggestions').hide();
    // });

    if (Storage !== undefined) {
      $(document).ready(function () {
        "use strict";

        var enabled = $("#viewlet-disclaimer").attr("data-enabled");
        if (enabled !== "true") {
          return;
        }

        var last_modified = $("#viewlet-disclaimer").attr("data-last-modified");
        var last_seen = localStorage.getItem("idgx.disclaimer");
        if (last_seen === null || last_seen < last_modified) {
          $("#viewlet-disclaimer").show();
        }

        $("button[name='idgx.disclaimer.ok']").click(function (event) {
          event.preventDefault();
          localStorage.setItem("idgx.disclaimer", last_modified);
          $("#viewlet-disclaimer").hide();
        });

      });
    }

  }
}
