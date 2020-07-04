'''表格解析示例'''

from renderer.utils import is_equal, parse_form

within = ('中标人', '中标单位', '中标供应商',
          '中标公司', '中标候选人', '成交人',
          '成交单位', '成交供应商')
without = ('浏览次数', '阅读次数', '访问次数',
           '发布时间')

url = 'http://www.nbzfcg.cn/project/zcyNotice_view.aspx?Id=726b40c9-1043-4aa5-bb5b-de6a90665b96'

url = 'http://www.jj.gov.cn/art/2017/8/24/art_1326298_9970195.html'
string = parse_form(url, within, without, to_list=False)
string

form = parse_form(url, within, without, to_list=True)
is_equal(form)
