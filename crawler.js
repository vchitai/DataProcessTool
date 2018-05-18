var page = require('webpage').create();
var user = []
var fs = require('fs');
var path = 'output.txt';
var link = []
/*
page.onConsoleMessage = function(msg) {
  console.log("[PAGE]" + msg);
}*/
/*
page.onResourceError = function(resourceError) {
    console.error('[DEBUG]'+resourceError.url + ': ' + resourceError.errorString);
};*/

function getDataFrom(now) {
	var url = link[now]
	console.log("Going to "+ url);
	page.open(url, function(status) {
		if (status !== 'success') {
			console.log('Load failed');
		}
		else {
			console.log(status);
			//phantom.exit();
			console.log('[DEBUG] Going to'+ url);
			var us = page.evaluate(function() {
				var un = []
				var ta = []
				$.each($(".username"), function(k,v) {
					un.push(v.innerHTML)
				})
				$.each($(".timeago"), function(k,v) {
					ta.push(v.innerHTML);
				})

				var us = []
				for (var i = 0; i<un.length; i++)
					us.push({
						username: un[i],
						timeago: ta[i]
					});
				return us;
			})
			for (var i = 0; i<us.length; i++)
				user.push(us[i])

			if (now < link.length-1) {
				console.log("[DEBUG] Recursive "+ url);
				getDataFrom(now+1)
			} else {
				fs.write(path, JSON.stringify(user), 'w');
				page.render("example.png");
				phantom.exit();
			}
			
		}
	})
}

//page.settings.userAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36';
page.open('http://khanviet.org/courses/course-v1:HCMUS+Python_Beginner+2018_T3/discussion/forum/', function(status) {
	console.log("Loging in...");
  if (status !== 'success') {
    console.log('Unable to access network');
  } else {
	page.evaluate(function() {
  		$("#login-email").val("chitai.vct@gmail.com");
  		$("#login-password").val("01218101076");
  		$(".login-button").click();
		});
	setTimeout(function() {
		page.evaluate(function() {
			$("#all_discussions span").click()
			//console.log("Clicked");
  		});
		setTimeout(function() {
			page.evaluate(function() {
				$(".forum-nav-load-more-link").click()	
			});
			setTimeout(function() {
				var a = page.evaluate(function() {
					var a = [];
					$.each($(".forum-nav-thread-link"), function(k, v) {a.push(v.href)});
					return a;
				});
				link = a;
				//console.log(link);

				getDataFrom(0);
			}, 1000)
	    }, 1000);
    }, 1000);

  }
});