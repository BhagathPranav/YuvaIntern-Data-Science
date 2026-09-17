def generate_relative_twb():
    twb_content = """<?xml version='1.0' encoding='utf-8' ?>

<!-- build 20261.26.0410.0924                               -->
<workbook original-version='18.1' source-build='2026.1.1 (20261.26.0410.0924)' source-platform='mac' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
  <preferences>
    <preference name='ui.encoding.shelf.height' value='24' />
    <preference name='ui.shelf.height' value='26' />
  </preferences>
  <datasources>
    <datasource caption='HR Analytics Cleaned' inline='true' name='textscan.1hr_cleaned' version='18.1'>
      <connection class='federated'>
        <named-connections>
          <named-connection caption='HR_Analytics_Cleaned' name='textscan.1hr_cleaned'>
            <connection class='textscan' directory='/Users/bhagath/Desktop/AIO/Yuva_intern' filename='HR_Analytics_Cleaned.csv' password='' server='' />
          </named-connection>
        </named-connections>
        <relation connection='textscan.1hr_cleaned' name='HR_Analytics_Cleaned.csv' table='[HR_Analytics_Cleaned#csv]' type='table'>
          <columns character-set='UTF-8' header='yes' locale='en_US' separator=','>
            <column datatype='integer' name='Age' ordinal='0' />
            <column datatype='string' name='Attrition' ordinal='1' />
            <column datatype='string' name='BusinessTravel' ordinal='2' />
            <column datatype='integer' name='DailyRate' ordinal='3' />
            <column datatype='string' name='Department' ordinal='4' />
            <column datatype='integer' name='DistanceFromHome' ordinal='5' />
            <column datatype='integer' name='Education' ordinal='6' />
            <column datatype='string' name='EducationField' ordinal='7' />
            <column datatype='integer' name='EnvironmentSatisfaction' ordinal='8' />
            <column datatype='string' name='Gender' ordinal='9' />
            <column datatype='integer' name='HourlyRate' ordinal='10' />
            <column datatype='integer' name='JobInvolvement' ordinal='11' />
            <column datatype='integer' name='JobLevel' ordinal='12' />
            <column datatype='string' name='JobRole' ordinal='13' />
            <column datatype='integer' name='JobSatisfaction' ordinal='14' />
            <column datatype='string' name='MaritalStatus' ordinal='15' />
            <column datatype='real' name='MonthlyIncome' ordinal='16' />
            <column datatype='string' name='SalarySlab' ordinal='17' />
            <column datatype='integer' name='MonthlyRate' ordinal='18' />
            <column datatype='integer' name='NumCompaniesWorked' ordinal='19' />
            <column datatype='string' name='OverTime' ordinal='20' />
            <column datatype='integer' name='PercentSalaryHike' ordinal='21' />
            <column datatype='integer' name='PerformanceRating' ordinal='22' />
            <column datatype='integer' name='RelationshipSatisfaction' ordinal='23' />
            <column datatype='integer' name='StockOptionLevel' ordinal='24' />
            <column datatype='integer' name='TotalWorkingYears' ordinal='25' />
            <column datatype='integer' name='TrainingTimesLastYear' ordinal='26' />
            <column datatype='integer' name='WorkLifeBalance' ordinal='27' />
            <column datatype='integer' name='YearsAtCompany' ordinal='28' />
            <column datatype='integer' name='YearsInCurrentRole' ordinal='29' />
            <column datatype='integer' name='YearsSinceLastPromotion' ordinal='30' />
            <column datatype='real' name='YearsWithCurrManager' ordinal='31' />
            <column datatype='integer' name='Attrition_Numeric' ordinal='32' />
            <column datatype='string' name='Age_Group' ordinal='33' />
            <column datatype='string' name='Tenure_Group' ordinal='34' />
          </columns>
        </relation>
      </connection>
      <layout dim-ordering='alphabetic' measure-ordering='alphabetic' show-structure='true' />
    </datasource>
  </datasources>
  <worksheets>
    <worksheet name='Sheet 1'>
      <table>
        <view>
          <datasources>
            <datasource caption='HR Analytics Cleaned' name='textscan.1hr_cleaned' />
          </datasources>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Automatic' />
          </pane>
        </panes>
        <rows />
        <cols />
      </table>
    </worksheet>
  </worksheets>
  <windows source-height='30'>
    <window class='worksheet' maximized='true' name='Sheet 1'>
      <cards>
        <edge name='left'>
          <strip size='160'>
            <card type='pages' />
            <card type='filters' />
            <card type='marks' />
          </strip>
        </edge>
        <edge name='top'>
          <strip size='2147483647'>
            <card type='columns' />
          </strip>
          <strip size='2147483647'>
            <card type='rows' />
          </strip>
        </edge>
      </cards>
    </window>
  </windows>
</workbook>
"""
    with open('/Users/bhagath/Desktop/AIO/Yuva_intern/HR_Analytics_Dashboard.twb', 'w', encoding='utf-8') as f:
        f.write(twb_content)
    print("Successfully generated relative clean HR_Analytics_Dashboard.twb")

if __name__ == "__main__":
    generate_relative_twb()
