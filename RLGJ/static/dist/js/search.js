function Search(){ 
        $.ajax({  
                cache: true,  
                type: "GET",  
                url:"localhost:8000/RLGJ/OnMessage/",  
                data:$('#saveReportForm').serialize(),// 你的formid  
                async: false,  
                error: function(request) {  
                    //错误处理
                },  
                success: function(data) {  
                    searchresult(data);  
                }  
            });
         return false;  

}
function searchresult(data){
	
	 html+='<li>';
	        	html+='<img src="'+data[key]['img']+'" alt="..." class="img-rounded">';
	           	html+='<div>';
	             	html+='<p>姓名：'+data[key]['name']+'</p>';
	            	html+=' <p>身份证号：'+data[key]['id_card']+'</p>';
	          	html+=' </div>';
	       	html+='  </li>';
}
