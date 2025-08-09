(base) wujingwei@LAPTOP-JHVV030O:~/foundry-cu/ragflow$ git remote -v
gitlab  git@125.122.154.130:wujingwei/ragflow.git (fetch)
gitlab  git@125.122.154.130:wujingwei/ragflow.git (push)
origin  ssh://git@github.com/infiniflow/ragflow.git (fetch)
origin  ssh://git@github.com/infiniflow/ragflow.git (push)
team_shu_lian   git@git.shu-lian.com:datainterconnect/ragflow (fetch)
team_shu_lian   git@git.shu-lian.com:datainterconnect/ragflow (push)



gh repo create ragflow --public
# 添加GitHub远程仓库
git remote add github ssh://git@github.com/WuJingweiPayton/ragflow.git 


git checkout -b main

git push github main
git push github dev

git remote -v

git add .




git commit  --no-verify -m "GPT-5修改之前的基准提交" 
git commit  --no-verify -m "请你在/chat里面补齐LLM调用MCP的能力，前后端代码改造都要有。首先你要分析现有代码，然后罗列出现有代码缺陷，列出修改步骤，然后按步骤修改现有代码。请开始。" 



git fetch team_shu_lian

# 基于当前分支创建新开发分支
git checkout -b dev

# 推送新分支到远程（首次推送需用 -u 建立跟踪）
git push -u team_shu_lian dev

git push -u gitlab dev

# 后续推送简化
git push


http://git.shu-lian.com:30080/users/sign_in
http://125.122.154.130:30080 wujingwei dfPvO1dYCpf2FRvD
git 地址和账号密码
