import os
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TWB_PATH = os.path.join(BASE_DIR, "HR_Analytics_Capstone_Dashboard.twb")
TWBX_PATH = os.path.join(BASE_DIR, "HR_Analytics_Capstone_Dashboard.twbx")
CSV_PATH = os.path.join(BASE_DIR, "HR_Analytics_Capstone.csv")

def create_tableau_capstone_xml():
    twb_content = """<?xml class='1.0' encoding='utf-8' ?>
<workbook original-version='18.1' source-build='2023.1.0' source-platform='mac' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
  <preferences>
    <preference name='ui.encoding.shelf.height' value='24' />
    <preference name='ui.shelf.height' value='26' />
  </preferences>
  <datasources>
    <datasource caption='HR Analytics Capstone' inline='true' name='federated.hr_capstone' version='18.1'>
      <connection class='federated'>
        <named-connections>
          <named-connection caption='HR_Analytics_Capstone' name='textscan.hr_capstone'>
            <connection class='textscan' directory='.' filename='HR_Analytics_Capstone.csv' password='' server='' />
          </named-connection>
        </named-connections>
      </connection>
      <column datatype='integer' name='[Cluster]' role='dimension' type='ordinal' />
      <column datatype='string' name='[Attrition]' role='dimension' type='nominal' />
      <column datatype='string' name='[Department]' role='dimension' type='nominal' />
      <column datatype='string' name='[JobRole]' role='dimension' type='nominal' />
      <column datatype='integer' name='[Age]' role='measure' type='quantitative' />
      <column datatype='integer' name='[MonthlyIncome]' role='measure' type='quantitative' />
      <column datatype='integer' name='[TotalWorkingYears]' role='measure' type='quantitative' />
      <column datatype='integer' name='[YearsAtCompany]' role='measure' type='quantitative' />
      <column datatype='real' name='[LogisticRegression_Prob]' role='measure' type='quantitative' />
      <column datatype='real' name='[NeuralNetwork_Prob]' role='measure' type='quantitative' />
      <layout dim-ordering='alphabetic' dim-percentage='0.5' measure-ordering='alphabetic' measure-percentage='0.5' show-structure='true' />
      <semantic-values>
        <semantic-value key='[Country].[Name]' value='&quot;United States&quot;' />
      </semantic-values>
    </datasource>
  </datasources>
  <worksheets>
    <worksheet name='Capstone Executive Dashboard'>
      <table>
        <view>
          <datasources>
            <datasource caption='HR Analytics Capstone' name='federated.hr_capstone' />
          </datasources>
          <datasource-dependencies datasource='federated.hr_capstone'>
            <column datatype='string' name='[Attrition]' role='dimension' type='nominal' />
            <column datatype='string' name='[Department]' role='dimension' type='nominal' />
            <column datatype='integer' name='[MonthlyIncome]' role='measure' type='quantitative' />
            <column datatype='integer' name='[TotalWorkingYears]' role='measure' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane>
            <slice>
              <strip size='160'>
                <card type='rows' />
                <card type='cols' />
              </strip>
            </slice>
            <mark class='Automatic' />
          </pane>
        </panes>
        <rows />
        <cols />
      </table>
    </worksheet>
  </worksheets>
  <dashboards>
    <dashboard name='Integrative Capstone HR Pipeline'>
      <style />
      <size maxheight='900' maxwidth='1400' minheight='900' minwidth='1400' />
      <zones>
        <zone h='100000' id='1' type-static='layout-basic' w='100000' x='0' y='0'>
          <zone h='98000' id='2' param='horiz' type-static='layout-flow' w='98000' x='1000' y='1000'>
            <zone h='96000' id='3' name='Capstone Executive Dashboard' w='96000' x='2000' y='2000' />
          </zone>
        </zone>
      </zones>
    </dashboard>
  </dashboards>
  <windows>
    <window class='dashboard' name='Integrative Capstone HR Pipeline'>
      <active pane-at-count='1' />
    </window>
  </windows>
</workbook>
"""
    with open(TWB_PATH, "w", encoding="utf-8") as f:
        f.write(twb_content)
    print(f"Created Tableau workbook file: {TWB_PATH}")

def package_twbx():
    with zipfile.ZipFile(TWBX_PATH, 'w', zipfile.ZIP_DEFLATED) as z:
        if os.path.exists(TWB_PATH):
            z.write(TWB_PATH, arcname="HR_Analytics_Capstone_Dashboard.twb")
        if os.path.exists(CSV_PATH):
            z.write(CSV_PATH, arcname="HR_Analytics_Capstone.csv")
    print(f"Created Tableau packaged workbook: {TWBX_PATH}")

if __name__ == "__main__":
    create_tableau_capstone_xml()
    package_twbx()
