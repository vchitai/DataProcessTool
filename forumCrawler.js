var page = require('webpage').create();
var args = require('system').args;
var user = [];
var fs = require('fs');
var link = [];
var usrname = args[1];
var password = args[2];
var rootUrl = args[3];
var path = args[4];
var path2 = 'test.txt'
var maxAttemp = 5;
/*
page.onConsoleMessage = function(msg) {
  console.log("[PAGE]" + msg);
}*/
page.onResourceError = function(resourceError) {
    page.reason = resourceError.errorString;
    page.reason_url = resourceError.url;
};

function getDataFrom(now, attempt) {
	var url = link[now]
	console.log("[DEBUG] Going to "+ url + " at " + attempt + " times");
    page = require("webpage").create();
	page.open(url, function(status) {
		console.log(status);
		if (status !== 'success') {
			console.log(
                "Error opening url \"" + page.reason_url
                + "\": " + page.reason
            );
            page.close();
			if (attempt < maxAttemp) {
				getDataFrom(now, attempt+1);
			} else {
				if (now < link.length-1) {
					getDataFrom(now+1, 0)
				} else {
					fs.write(path, JSON.stringify(user), 'w');
					phantom.exit();
				}
			}
		}
		else {
			var us = page.evaluate(function() {
				var un = []
				var ta = []
				$.each($(".username"), function(k,v) {
					un.push(v.innerHTML)
				})
				$.each($(".timeago"), function(k,v) {
					ta.push(v.innerHTML);
				})

				var usr = []
				for (var i = 0; i<un.length; i++)
					usr.push({
						username: un[i],
						timeago: ta[i]
					});
				return usr;
			})
			for (var i = 0; i<us.length; i++)
				user.push(us[i])	
			//fs.write(path2, JSON.stringify(us), 'a');
			page.close();
			if (now < link.length-1) {
				getDataFrom(now+1, 0)
			} else {
				fs.write(path, JSON.stringify(user), 'w');
				phantom.exit();
			}
		}

	})
}

page.settings.resourceTimeout = 10000;

//page.settings.userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36';
page.open(rootUrl, function(status) {
	console.log("Loging in...");
  if (status !== 'success') {
    console.log('Unable to access network');
  } else {
	page.evaluate(function(usrname, password) {
  		$("#login-email").val(usrname);
  		$("#login-password").val(password);
  		$(".login-button").click();
		}, usrname, password);
	setTimeout(function() {
		page.evaluate(function() {
			$("#all_discussions span").click()
  		});
		setTimeout(function() {
//			page.evaluate(function() {
//				$(".forum-nav-load-more-link").click()	
//			});
//			setTimeout(function() {
			var a = page.evaluate(function() {
				var a = [];
				$.each($(".forum-nav-thread-link"), function(k, v) {a.push(v.href)});
				return a;
			});
			link = a;
			page.close();
			getDataFrom(0, 0);
//			}, 1000)
	    }, 2000);
    }, 1000);

  }
});