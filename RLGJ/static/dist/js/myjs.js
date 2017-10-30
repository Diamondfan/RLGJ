var ulcontent=document.getElementById('imageul');
var name=null;
$(document).ready(function(){
	getall();
})

function getall(page,name){
	var query={
		currpage:page||1,
	}
	if(name){
		query['name']=name;
	}
	$.get("../../RLGJ/OnMessage/",query,function(result){
		var data=result['img'];
		var html='';
		for(var key in data){
	        html+='<li>';
	        	html+='<img src="'+data[key]['img']+'" alt="..." class="img-rounded">';
	           	html+='<div>';
	             	html+='<p>姓名：'+data[key]['name']+'</p>';
	            	html+=' <p>身份证号：'+data[key]['id_card']+'</p>';
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
