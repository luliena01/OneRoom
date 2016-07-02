function getRequestParam(id) {
    var query_string = {};
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
            // If first entry with this name
//        if (typeof query_string[pair[0]] === "undefined") {
//            query_string[pair[0]] = decodeURIComponent(pair[1]);
//            // If second entry with this name
//        } else
        if(pair[0] == id) {
            if (typeof pair[0] === "string") {
                return decodeURIComponent(pair[1]);
            }
        }
    }
    //return query_string;
};
