/*
var obj = {
    args:{
        pageCount:data.totalpage, // 总页
        current:data.currpage,    // 当前页
        backFn:'gopage'     //  回调
    }
}
pagefun = pageDom(obj)
 */

(function(w,d){
    function page(obj){
        this.backFn = obj.backFn;
        this.args = obj.args;
        this.id = obj.id || '_data_page';
    }

    page.prototype.init = function(obj){
        if(obj)this.args = obj;
        var dom = d.getElementById(this.id);
       
        dom.innerHTML = '<ul id="page" class="v page" >'+this.html()+'</ul>';
    }

    page.prototype.html = function(){
        var args = this.args;
        var html = '';
        if(args.pageCount == 0) return html;
        //上一页
        if(args.current > 1){
            html += '<li><a href="javascript:;" ipage="'+(parseInt(args.current) - 1)+'" class="v btn bdr _gopage">上一页</a></li>';
        }else{
            html += '<li><a href="javascript:;" class="v btn disabled bdr">上一页</a></li>';
        }
        //中间页码
        if(args.current != 1 && args.current >= 4 && args.pageCount != 4){
            html += '<li><a href="javascript:;" ipage="1" class="v btn _gopage">'+1+'</a></li>';
        }
        if(args.current-2 > 2 && args.current <= args.pageCount && args.pageCount > 5){
            html += '<li><a href="javascript:;" class="v btn">…</a></li>';
        }
        var start = args.current -2,end = args.current +2;
        if((start > 1 && args.current < 4)||args.current == 1){
            end++;
        }
        if(args.current > args.pageCount-4 && args.current >= args.pageCount){
            start--;
        }
        for (;start <= end; start++) {
            if(start <= args.pageCount && start >= 1){
                if(start != args.current){
                    html += '<li><a href="javascript:;" ipage="'+start+'" class="v btn _gopage">'+ start +'</a></li>';
                }else{
                    html += '<li><a href="javascript:;" class="v btn blue ">'+ start +'</a></li>';
                }
            }
        }
        if((args.current + 2 < args.pageCount - 1 )&& args.current >= 1 && args.pageCount > 5){
            html += '<li><a href="javascript:;" class="v btn">…</a></li>';
        }
        if(args.current != args.pageCount && args.current < args.pageCount -2  && args.pageCount != 4){
            html += '<li><a href="javascript:;" ipage="'+args.pageCount+'" class="v btn _gopage">'+args.pageCount+'</a></li>';
        }
        //下一页
        if(args.current < args.pageCount){
            html += '<li><a href="javascript:;" ipage="'+(parseInt(args.current) + 1)+'" class="v btn bdr _gopage">下一页</a></li>';
        }else{
            html += '<li><a href="javascript:;" class="v btn disabled bdr">下一页</a></li>';
        }

        return html;
    }

    w.pageDom = function(obj){
        return new page(obj);
    }
})(window,document);
