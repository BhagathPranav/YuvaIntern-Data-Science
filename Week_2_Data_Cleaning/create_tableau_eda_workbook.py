import zipfile
import uuid
import os

def build_week2_tableau_files():
    ws1_uuid = f"{{{uuid.uuid4()}}}".upper()
    ws2_uuid = f"{{{uuid.uuid4()}}}".upper()
    ws3_uuid = f"{{{uuid.uuid4()}}}".upper()
    ws4_uuid = f"{{{uuid.uuid4()}}}".upper()
    dash_uuid = f"{{{uuid.uuid4()}}}".upper()

    twb_content = f"""<?xml version='1.0' encoding='utf-8' ?>

<!-- build 20261.26.0410.0924                               -->
<workbook original-version='18.1' source-build='2026.1.1 (20261.26.0410.0924)' source-platform='mac' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
  <document-format-change-manifest>
    <AccessibleZoneTabOrder />
    <AnimationOnByDefault />
    <AutoCreateAndUpdateDSDPhoneLayouts />
    <MarkAnimation />
    <ObjectModelEncapsulateLegacy />
    <ObjectModelTableType />
    <SchemaViewerObjectModel />
    <SetMembershipControl />
    <SheetIdentifierTracking />
    <WindowsPersistSimpleIdentifiers />
  </document-format-change-manifest>
  <preferences>
    <preference name='ui.encoding.shelf.height' value='24' />
    <preference name='ui.shelf.height' value='26' />
  </preferences>
  <datasources>
    <datasource caption='HR Analytics Cleaned' inline='true' name='textscan.1hr_cleaned' version='18.1'>
      <connection class='federated'>
        <named-connections>
          <named-connection caption='HR_Analytics_Cleaned' name='textscan.1hr_cleaned'>
            <connection class='textscan' directory='/Users/bhagath/Desktop/AIO/Yuva_intern/Week_1_Data_Cleaning' filename='HR_Analytics_Cleaned.csv' password='' server='' />
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
    <!-- Sheet 1: Attrition Class Imbalance -->
    <worksheet name='Class Imbalance Countplot'>
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
            <view><breakdown value='auto' /></view>
            <mark class='Automatic' />
          </pane>
        </panes>
        <rows>[textscan.1hr_cleaned].[none:Attrition:nk]</rows>
        <cols>[textscan.1hr_cleaned].[sum:Attrition_Numeric:qk]</cols>
      </table>
      <simple-id uuid='{ws1_uuid}' />
    </worksheet>

    <!-- Sheet 2: Loyalty Penalty Scatter Plot -->
    <worksheet name='Loyalty Penalty Scatter'>
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
            <view><breakdown value='auto' /></view>
            <mark class='Automatic' />
          </pane>
        </panes>
        <rows>[textscan.1hr_cleaned].[avg:MonthlyIncome:qk]</rows>
        <cols>[textscan.1hr_cleaned].[avg:TotalWorkingYears:qk]</cols>
      </table>
      <simple-id uuid='{ws2_uuid}' />
    </worksheet>

    <!-- Sheet 3: Monthly Income Boxplot -->
    <worksheet name='Income Anomaly Boxplot'>
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
            <view><breakdown value='auto' /></view>
            <mark class='Automatic' />
          </pane>
        </panes>
        <rows>[textscan.1hr_cleaned].[none:Attrition:nk]</rows>
        <cols>[textscan.1hr_cleaned].[avg:MonthlyIncome:qk]</cols>
      </table>
      <simple-id uuid='{ws3_uuid}' />
    </worksheet>

    <!-- Sheet 4: Department Attrition Bar -->
    <worksheet name='Department Attrition Bar'>
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
            <view><breakdown value='auto' /></view>
            <mark class='Automatic' />
          </pane>
        </panes>
        <rows>[textscan.1hr_cleaned].[none:Department:nk]</rows>
        <cols>[textscan.1hr_cleaned].[sum:Attrition_Numeric:qk]</cols>
      </table>
      <simple-id uuid='{ws4_uuid}' />
    </worksheet>
  </worksheets>

  <dashboards>
    <dashboard enable-sort-zone-taborder='true' name='HR Attrition EDA Diagnostic Master Dashboard'>
      <style />
      <size maxheight='1000' maxwidth='1600' minheight='800' minwidth='1000' />
      <zones>
        <zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>
          <zone h='50000' id='2' name='Class Imbalance Countplot' w='50000' x='0' y='0' />
          <zone h='50000' id='3' name='Loyalty Penalty Scatter' w='50000' x='50000' y='0' />
          <zone h='50000' id='4' name='Income Anomaly Boxplot' w='50000' x='0' y='50000' />
          <zone h='50000' id='5' name='Department Attrition Bar' w='50000' x='50000' y='50000' />
        </zone>
      </zones>
      <simple-id uuid='{dash_uuid}' />
    </dashboard>
  </dashboards>

  <windows source-height='30'>
    <window class='worksheet' name='Class Imbalance Countplot'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
      <simple-id uuid='{ws1_uuid}' />
    </window>
    <window class='worksheet' name='Loyalty Penalty Scatter'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
      <simple-id uuid='{ws2_uuid}' />
    </window>
    <window class='worksheet' name='Income Anomaly Boxplot'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
      <simple-id uuid='{ws3_uuid}' />
    </window>
    <window class='worksheet' name='Department Attrition Bar'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
      <simple-id uuid='{ws4_uuid}' />
    </window>
    <window class='dashboard' maximized='true' name='HR Attrition EDA Diagnostic Master Dashboard'>
      <cards><edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge></cards>
      <simple-id uuid='{dash_uuid}' />
    </window>
  </windows>
</workbook>
"""

    twb_path = "/Users/bhagath/Desktop/AIO/Yuva_intern/Week_2_Data_Cleaning/HR_Analytics_EDA_Dashboard.twb"
    twbx_path = "/Users/bhagath/Desktop/AIO/Yuva_intern/Week_2_Data_Cleaning/HR_Analytics_EDA_Dashboard.twbx"
    csv_path = "/Users/bhagath/Desktop/AIO/Yuva_intern/Week_1_Data_Cleaning/HR_Analytics_Cleaned.csv"

    # Write .twb
    with open(twb_path, 'w', encoding='utf-8') as f:
        f.write(twb_content)

    # Package into .twbx
    with zipfile.ZipFile(twbx_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('HR_Analytics_EDA_Dashboard.twb', twb_content)
        if os.path.exists(csv_path):
            zf.write(csv_path, 'Data/HR_Analytics_Cleaned/HR_Analytics_Cleaned.csv')

    print(f"Successfully generated Week 2 Tableau .twb & .twbx at:\n{twb_path}\n{twbx_path}")

if __name__ == "__main__":
    build_week2_tableau_files()
