import coverage
import pytest
 
# Instantiating an object实例化对象
cov = coverage.coverage()
cov.start()
 
# test测试
pytest.main(["-v", "-s"])
 
# End of analysis结束分析
cov.stop()
 
# Save the results结果保存
cov.save()
 
# The command line mode displays the results and the specific number of unexecuted code lines for viewing test results.命令行模式展示结果,并展示未执行代码具体行数，用于测试结果查看使用
cov.report(show_missing=True)
 
# Generate HTML coverage results report生成HTML覆盖率结果报告
cov.html_report(directory="res_html")