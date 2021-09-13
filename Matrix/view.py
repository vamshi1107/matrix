from  django.shortcuts import *
from  django.http import *
from sub.models import  *
from sub.models import request as req
import urllib

def index(request):
    member.objects.filter(username="").delete()
    if not request.session.get("login",False) :
        return  redirect("login")
    ul = list(relation.objects.filter(user1=request.session.get("user", "")).values_list("user2", flat=True)) + \
         list(relation.objects.filter(user2=request.session.get("user", "")).values_list("user1", flat=True))
    lou=request.session["user"]
    pl=[]
    for i in post.objects.all()[::-1]:
        if i.user in ul:
            d = {}
            d["comments"]=comment.objects.filter(postid=i.id)
            d["ncom"]=len(comment.objects.filter(postid=i.id))
            d["post"]=i
            v=member.objects.filter(username=i.user)
            dp = displaypic.objects.filter(user=i.user)
            if len(dp)>0:
               d["dp"]=dp[0]
               d["dpfound"]=True
            else:
                d["dpfound"] = False
            if len(v)>0:
               d["user"]=v[0]
            pl.append(d)
    loginu=member.objects.filter(username=lou)[0]
    logindp=displaypic.objects.filter(user=lou)
    if len(logindp)>0:
        dp=logindp[0].content
    else:
        dp ="https://instagram.fdel12-1.fna.fbcdn.net/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=instagram.fdel12-1.fna.fbcdn.net&_nc_ohc=0CE398PqtLwAX9XWgt3&oh=b03f38f512349bed45a72c144cd6720d&oe=6077A18F&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2"

    sugs=get_sugs(lou)[:5]
    return render(request,"container.html",context={"posts":pl,"user":lou,"loginuser":loginu,"dp":dp,"sugs":sugs})

def get_sugs(name):
     ul = list(relation.objects.filter(user1=name).values_list("user2", flat=True)) + \
         list(relation.objects.filter(user2=name).values_list("user1", flat=True))
     l=[]
     for i in ul:
         il = list(relation.objects.filter(user1=i).values_list("user2", flat=True)) + \
              list(relation.objects.filter(user2=i).values_list("user1", flat=True))
         for j in il:
             if j not in ul and not j==name:
                d={}
                d["user"]=member.objects.filter(username=j)[0]
                dp = displaypic.objects.filter(user=j)
                if len(dp) > 0:
                   d["dp"] = dp[0].content
                else:
                   d["dp"] = "https://instagram.fdel12-1.fna.fbcdn.net/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=instagram.fdel12-1.fna.fbcdn.net&_nc_ohc=0CE398PqtLwAX9XWgt3&oh=b03f38f512349bed45a72c144cd6720d&oe=6077A18F&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2"
                l.append(d)
     return l

def profile(request):
    if not request.session.get("login", False):
        return redirect("login")
    user=request.session.get("user","")
    if user=="":
        request.session.flush()
        return  redirect("login")
    u=member.objects.filter(username=user)
    ul = list(relation.objects.filter(user1=request.session.get("user", "")).values_list("user2", flat=True)) + \
         list(relation.objects.filter(user2=request.session.get("user", "")).values_list("user1", flat=True))
    pl=post.objects.filter(user=request.session.get("user",""))
    dp=displaypic.objects.filter(user=user)
    if len(dp)>0:
        dk=dp[0]
        dp_found = True
    else:
        dk="/"
        dp_found = False
    if len(u)>0:
        loguser=u[0]
        return render(request,"profile.html",context={"user":loguser,"friends":len(ul),"posts":pl,"nposts":len(pl),"dp":dk,"dpfound":dp_found})
    else:
        request.session.flush()
        return redirect("login")

def login(request):
    if request.method=="POST":
          p = request.POST["pass"]
          u = str(request.POST["username"]).lower()
          o=member.objects.filter(username=u,password=p)
          if len(o) >0:
              request.session["login"]=True
              request.session.set_expiry(0)
              print(request.session.get_expire_at_browser_close())
              print(request.session.get_expiry_date())
              request.session["user"]=u
              return redirect("index")
          else:
              return render(request, "login.html")
    return  render(request,"login.html")

def register(request):
    return  render(request,"register.html")

def new_user(request):
    u = request.POST["username"]
    o = member.objects.filter(username=u)
    if len(o) > 0:
        return redirect("register")
    else:
        u=member(name=request.POST["name"],password=request.POST["pass"],username=str(request.POST["username"]).lower(),email=request.POST["email"])
        u.save()
        return redirect("login")

def logout(request):
    if request.session["login"]:
         request.session["login"]=False
         request.session["user"]=""
         request.session.flush()
         return redirect("login")
    else:
        return redirect("index")


def user_data(request):
    if request.GET.get("code","00007") == "1107":
        users=list(member.objects.values())
        return JsonResponse({"users":users},safe=False)
    else:
        return redirect("index")

def search(request):
    if not request.session.get("login",False) :
        return  redirect("login")
    return  render(request,"search.html")

def userpage(request,user):
    if not request.session.get("login",False) :
        return  redirect("login")
    u=member.objects.filter(username=user)
    check = req.objects.filter(To=user, From=request.session["user"])
    ul = list(relation.objects.filter(user1=request.session.get("user", "")).values_list("user2", flat=True)) + \
         list(relation.objects.filter(user2=request.session.get("user", "")).values_list("user1", flat=True))
    pl = post.objects.filter(user=user)
    uf = list(relation.objects.filter(user1=user).values_list("user2", flat=True)) + \
         list(relation.objects.filter(user2=user).values_list("user1", flat=True))
    dp=displaypic.objects.filter(user=user)
    if len(dp) > 0:
        dk = dp[0]
        dp_found = True
    else:
        dk = "/"
        dp_found = False
    if user in ul:
        friend=True
    else:
        friend=False
    if len(check)>0:
        requested=True
    else:
        requested=False
    if len(u)>0:
        if u[0].username == request.session["user"]:
            iu=True
        else:
            iu=False
        return render(request,"userpage.html",{"user":u[0],"isuser":iu,
                                               "loguser":request.session["user"],
                                               "requested":requested,"friend":friend,"posts":pl,
                                               "nposts":len(pl),"nfriends":len(uf),
                                               "dp":dk,"dpfound":dp_found
                                               })
    else:
        return redirect("search")


def friends(request):
    res=req.objects.filter(To=request.session.get("user","")).values_list('From', flat=True)
    us=member.objects.filter(username__icontains=res)
    ul=list(relation.objects.filter(user1=request.session.get("user","")).values_list("user2",flat=True))+\
             list(relation.objects.filter(user2=request.session.get("user","")).values_list("user1",flat=True))
    flist=[]
    for i in ul:
        flist+=member.objects.filter(username=i)
    if len(res)>0:
       return render(request,"friends.html",context={"req":us,"found":True,"loguser":request.session.get("user",""),"friends":flist})
    else:
        return render(request, "friends.html", context={"found": False,"loguser":request.session.get("user",""),"friends":flist})


def send_request(request):
    f = request.GET["From"]
    t = request.GET["To"]
    check=req.objects.filter(To=t, From=f)
    if len(check)>0:
        return HttpResponse("True")
    r=req(To=t,From=f)
    r.save()
    return HttpResponse("True")

def add_friend(request):
    u1=request.GET.get("user1")
    u2=request.GET.get("user2")
    rc=relation.objects.filter(user1=u1,user2=u2)
    rc2=relation.objects.filter(user2=u1,user1=u2)
    if len(rc)>0 or len(rc2)>0 :
        return HttpResponse("True")
    r=relation(user1=u1,user2=u2)
    r.save()
    ck=req.objects.filter(To=u2, From=u1)
    if len(ck)>0:
           req.objects.filter(To=u2,From=u1).delete()
    return HttpResponse("True")


def remove(request):
    u1 = request.GET.get("u1")
    u2 = request.GET.get("u2")
    ul = list(relation.objects.filter(user1=u1,user2=u2).values_list("user2", flat=True)) + \
         list(relation.objects.filter(user2=u1,user1=u2).values_list("user1", flat=True))
    if len(ul)>0:
        relation.objects.filter(user1=u1,user2=u2).delete()
        relation.objects.filter(user2=u1,user1=u2).delete()
        return HttpResponse("True")
    else:
        return HttpResponse("True")

def remove_request(request):
        f = request.GET["From"]
        t = request.GET["To"]
        check = req.objects.filter(To=t, From=f)
        if len(check) > 0:
            req.objects.filter(To=t, From=f).delete()
            return HttpResponse("True")
        r = req(To=t, From=f).delete()
        r.save()
        return HttpResponse("True")

def show_friends(request,user):
    ul = list(relation.objects.filter(user1=user).values_list("user2", flat=True)) + \
         list(relation.objects.filter(user2=user).values_list("user1", flat=True))
    flist = []
    for i in ul:
        flist += member.objects.filter(username=i)
    return render(request,"userfriends.html",context={"friends":flist})

def newpost(request):
    post.objects.filter(user="").delete()
    u=request.POST.get("user","")
    url=request.POST.get("url","")
    t=request.POST.get("type","")
    cap=request.POST.get("cap","")
    p=post(user=u,caption=cap,content=url,type=t)
    p.save()
    return redirect("profile")

def check(request,user):
    u=member.objects.filter(username=user)
    if len(u)>0:
        return HttpResponse("True")
    else:
        return HttpResponse("False")

def add_pic(request):
    u = request.POST.get("user", "")
    url = request.POST.get("url", "")
    dp=displaypic.objects.filter(user=u)
    if len(dp)>0:
        du= displaypic.objects.filter(user=u).update(content=url)
        return redirect("profile")
    d = displaypic(user=u,content=url)
    d.save()
    return redirect("profile")


def remove_post(request,id):
    post.objects.filter(id=id).delete()
    return HttpResponse("True")

def caption(reuest,id):
    c=post.objects.filter(id=id).values_list("caption",flat=True)
    return HttpResponse(c)

def validate(reuest,user):
    c=member.objects.filter(username=user)
    if len(c)>0:
        return HttpResponse("False")
    else:
        return HttpResponse("True")

def add_comment(request):
    id = request.GET["id"]
    user = request.GET["user"]
    comm = request.GET["comm"]
    c=comment(user=user,content=comm,postid=id)
    c.save()
    return HttpResponse("True")

def get_comment(request,code):
    if code==1107:
        id = request.GET["id"]
        c=[]
        comms=comment.objects.filter(postid=id)
        for i in comms:
            d={}
            d["content"]=i.content
            u=member.objects.filter(username=i.user)
            if len(u)>0:
               d["username"]=u[0].username
               dp  = displaypic.objects.filter(user=u[0].username)
               if len(dp)>0:
                    d["dp"]=dp[0].content
               else:
                    d["dp"] ="https://instagram.fdel12-1.fna.fbcdn.net/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=instagram.fdel12-1.fna.fbcdn.net&_nc_ohc=0CE398PqtLwAX9XWgt3&oh=b03f38f512349bed45a72c144cd6720d&oe=6077A18F&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2"
            c.append(d)
        return  JsonResponse(c,safe=False)
    else:
         return HttpResponse("False")
