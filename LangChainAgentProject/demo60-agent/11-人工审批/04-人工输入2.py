from langchain_community.callbacks import HumanApprovalCallbackHandler
from langchain_community.tools import ShellTool

tool = ShellTool(callbacks=[HumanApprovalCallbackHandler()])
tool.run('ls')