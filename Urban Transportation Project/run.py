import coverage
import pytest
 
# 实例化对象
cov = coverage.coverage()
cov.start()
 
# 测试
pytest.main(["-v", "-s"])
 
# 结束分析
cov.stop()
 
# 结果保存
cov.save()
 
# 命令行模式展示结果,并展示未执行代码具体行数，用于测试结果查看使用
cov.report(show_missing=True)
 
# 生成HTML覆盖率结果报告
cov.html_report(directory="res_html")