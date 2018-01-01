var ulcontent=document.getElementById('imageul');
var name=null;
var layout = document.getElementById("layout");
var box = document.getElementById("box");
var closed = document.getElementById("closed");
var button = document.getElementById("button");
var timecontent = document.getElementById("timecontent");
var globalid = 0;
$(document).ready(function(){
	getall();
	$("#imageul").delegate("li","click",function(event){
                  var target = $(this);
                  var status=target.attr("status");
				  globalid=target.prop("id");
				  if(status){
					layout.style.display = "block"; 
					box.style.display = "block";  
				  }
    })
})


layout.onclick = function() { 
        layout.style.display = "none"; 
        box.style.display = "none"; 
}
$('#closed').on('click',function() {
    layout.style.display = "none"; 
        box.style.display = "none"; 
 });

function getall(page,name){
	var query={
		currpage:page||1,
	}
	if(name){
		query['name']=name;
    }
	$.get("../../RLGJ/OnSelect/",query,function(result){
        var data=result['img'];
        var html='';
		for(var key in data){
		
	        html+='<li id="'+data[key]['id_card']+'" status="'+data[key]['status']+'">';
		      	html+='<img src="'+data[key]['img']+'" alt="..." class="img-rounded">';
	           	html+='<div>';
	             	html+='<p>姓名：'+data[key]['name']+'</p>';
	            	html+='<p>身份证号：'+data[key]['id_card']+'</p>';
					html+='<p>添加日期：</br>'+data[key]['addtime']+'</p>'
	          	html+=' </div>';
	       	html+='  </li>';
		}
		ulcontent.innerHTML=html;
		var obj = {
		    args:{
		        pageCount:result.totalpage, // 总页
		        current:result.currpage,    // 当前
		    },
		    id:'pagebox'
		}
		var pagefun = pageDom(obj);
		pagefun.init();

	})
}



$("body").click(function(event){
	var $this = $(event.target);
	var page=$this.attr("ipage");
	if(page){
		getall(page,name);
	}
})

function Search(){ 
	name=$("#inputname").val();
	getall(1,name)
    return false;  
}
