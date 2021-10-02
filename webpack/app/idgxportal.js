import BugFix from './js/bugfix.js';
import SearchSuggestions from './js/search_suggestions.js';
import TipPreview from './js/tippreview.js';
import Disclaimer from './js/disclaimer.js';


// https://hacks.mozilla.org/2015/04/es6-in-depth-iterators-and-the-for-of-loop/
jQuery.prototype[Symbol.iterator] = Array.prototype[Symbol.iterator];


$(() => {
  new BugFix();
  new SearchSuggestions();
  new Disclaimer();
  if ($('[data-tippreview-enabled="true"]').length > 0) {
    new TipPreview();
  };
});


export default {
  BugFix,
  SearchSuggestions,
  TipPreview,
  Disclaimer,
}
