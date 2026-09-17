import zipfile
import os
import uuid

def build_twbx():
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
    <datasource caption='HR Analytics Cleaned' inline='true' name='federated.1hr_analytics' version='18.1'>
      <connection class='federated'>
        <named-connections>
          <named-connection caption='HR_Analytics_Cleaned' name='textscan.1hr_cleaned'>
            <connection class='textscan' directory='Data/HR_Analytics_Cleaned' filename='HR_Analytics_Cleaned.csv' password='' server='' />
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
        <cols>
          <map key='[Age]' value='[HR_Analytics_Cleaned.csv].[Age]' />
          <map key='[Attrition]' value='[HR_Analytics_Cleaned.csv].[Attrition]' />
          <map key='[BusinessTravel]' value='[HR_Analytics_Cleaned.csv].[BusinessTravel]' />
          <map key='[Department]' value='[HR_Analytics_Cleaned.csv].[Department]' />
          <map key='[EducationField]' value='[HR_Analytics_Cleaned.csv].[EducationField]' />
          <map key='[Gender]' value='[HR_Analytics_Cleaned.csv].[Gender]' />
          <map key='[JobRole]' value='[HR_Analytics_Cleaned.csv].[JobRole]' />
          <map key='[MaritalStatus]' value='[HR_Analytics_Cleaned.csv].[MaritalStatus]' />
          <map key='[MonthlyIncome]' value='[HR_Analytics_Cleaned.csv].[MonthlyIncome]' />
          <map key='[OverTime]' value='[HR_Analytics_Cleaned.csv].[OverTime]' />
          <map key='[SalarySlab]' value='[HR_Analytics_Cleaned.csv].[SalarySlab]' />
          <map key='[YearsAtCompany]' value='[HR_Analytics_Cleaned.csv].[YearsAtCompany]' />
          <map key='[YearsSinceLastPromotion]' value='[HR_Analytics_Cleaned.csv].[YearsSinceLastPromotion]' />
          <map key='[Attrition_Numeric]' value='[HR_Analytics_Cleaned.csv].[Attrition_Numeric]' />
        </cols>
      </connection>
      <aliases enabled='yes' />
      <column datatype='integer' name='[Attrition_Numeric]' role='measure' type='quantitative' />
      <column caption='Attrition Rate' datatype='real' name='[Calculation_AttrRate]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='SUM([Attrition_Numeric]) / COUNT([HR_Analytics_Cleaned.csv])' />
      </column>
      <layout dim-ordering='alphabetic' measure-ordering='alphabetic' show-structure='true' />
      <semantic-values>
        <semantic-value key='[Country].[Name]' value='&quot;United States&quot;' />
      </semantic-values>
    </datasource>
  </datasources>

  <actions />

  <worksheets>
    <!-- Sheet 1: Department Attrition Bar Chart -->
    <worksheet name='Department Attrition Bar'>
      <table>
        <view>
          <datasources>
            <datasource caption='HR Analytics Cleaned' name='federated.1hr_analytics' />
          </datasources>
          <datasource-dependencies datasource='federated.1hr_analytics'>
            <column datatype='integer' name='[Attrition_Numeric]' role='measure' type='quantitative' />
            <column datatype='string' name='[Department]' role='dimension' type='nominal' />
            <column-instance column='[Department]' derivation='None' name='[none:Department:nk]' pivot='key' type='nominal' />
            <column-instance column='[Attrition_Numeric]' derivation='Sum' name='[sum:Attrition_Numeric:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Bar' />
            <encodings>
              <color column='[federated.1hr_analytics].[none:Department:nk]' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.1hr_analytics].[none:Department:nk]</rows>
        <cols>[federated.1hr_analytics].[sum:Attrition_Numeric:qk]</cols>
      </table>
      <simple-id uuid='{ws1_uuid}' />
    </worksheet>

    <!-- Sheet 2: Education Field Attrition -->
    <worksheet name='Education Field Attrition'>
      <table>
        <view>
          <datasources>
            <datasource caption='HR Analytics Cleaned' name='federated.1hr_analytics' />
          </datasources>
          <datasource-dependencies datasource='federated.1hr_analytics'>
            <column datatype='integer' name='[Attrition_Numeric]' role='measure' type='quantitative' />
            <column datatype='string' name='[EducationField]' role='dimension' type='nominal' />
            <column-instance column='[EducationField]' derivation='None' name='[none:EducationField:nk]' pivot='key' type='nominal' />
            <column-instance column='[Attrition_Numeric]' derivation='Sum' name='[sum:Attrition_Numeric:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Pie' />
            <encodings>
              <color column='[federated.1hr_analytics].[none:EducationField:nk]' />
              <size column='[federated.1hr_analytics].[sum:Attrition_Numeric:qk]' />
            </encodings>
          </pane>
        </panes>
        <rows />
        <cols />
      </table>
      <simple-id uuid='{ws2_uuid}' />
    </worksheet>

    <!-- Sheet 3: OverTime Risk Bar Chart -->
    <worksheet name='OverTime Attrition Bar'>
      <table>
        <view>
          <datasources>
            <datasource caption='HR Analytics Cleaned' name='federated.1hr_analytics' />
          </datasources>
          <datasource-dependencies datasource='federated.1hr_analytics'>
            <column datatype='integer' name='[Attrition_Numeric]' role='measure' type='quantitative' />
            <column datatype='string' name='[OverTime]' role='dimension' type='nominal' />
            <column-instance column='[OverTime]' derivation='None' name='[none:OverTime:nk]' pivot='key' type='nominal' />
            <column-instance column='[Attrition_Numeric]' derivation='Sum' name='[sum:Attrition_Numeric:qk]' pivot='key' type='quantitative' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Bar' />
            <encodings>
              <color column='[federated.1hr_analytics].[none:OverTime:nk]' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.1hr_analytics].[none:OverTime:nk]</rows>
        <cols>[federated.1hr_analytics].[sum:Attrition_Numeric:qk]</cols>
      </table>
      <simple-id uuid='{ws3_uuid}' />
    </worksheet>

    <!-- Sheet 4: Salary Slabs Bar Chart -->
    <worksheet name='Income Slabs Bar Chart'>
      <table>
        <view>
          <datasources>
            <datasource caption='HR Analytics Cleaned' name='federated.1hr_analytics' />
          </datasources>
          <datasource-dependencies datasource='federated.1hr_analytics'>
            <column datatype='real' name='[MonthlyIncome]' role='measure' type='quantitative' />
            <column datatype='string' name='[SalarySlab]' role='dimension' type='nominal' />
            <column-instance column='[MonthlyIncome]' derivation='Avg' name='[avg:MonthlyIncome:qk]' pivot='key' type='quantitative' />
            <column-instance column='[SalarySlab]' derivation='None' name='[none:SalarySlab:nk]' pivot='key' type='nominal' />
          </datasource-dependencies>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane selection-relaxation-option='selection-relaxation-allow'>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Bar' />
            <encodings>
              <color column='[federated.1hr_analytics].[none:SalarySlab:nk]' />
            </encodings>
          </pane>
        </panes>
        <rows>[federated.1hr_analytics].[none:SalarySlab:nk]</rows>
        <cols>[federated.1hr_analytics].[avg:MonthlyIncome:qk]</cols>
      </table>
      <simple-id uuid='{ws4_uuid}' />
    </worksheet>
  </worksheets>

  <dashboards>
    <dashboard enable-sort-zone-taborder='true' name='HR Analytics Executive Master Dashboard'>
      <style />
      <size maxheight='1000' maxwidth='1600' minheight='800' minwidth='1000' />
      <zones>
        <zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>
          <zone h='50000' id='2' name='Department Attrition Bar' w='50000' x='0' y='0' />
          <zone h='50000' id='3' name='Education Field Attrition' w='50000' x='50000' y='0' />
          <zone h='50000' id='4' name='OverTime Attrition Bar' w='50000' x='0' y='50000' />
          <zone h='50000' id='5' name='Income Slabs Bar Chart' w='50000' x='50000' y='50000' />
        </zone>
      </zones>
      <simple-id uuid='{dash_uuid}' />
    </dashboard>
  </dashboards>

  <windows source-height='30'>
    <window class='worksheet' name='Department Attrition Bar'>
      <cards>
        <edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge>
        <edge name='top'><strip size='2147483647'><card type='columns' /></strip><strip size='2147483647'><card type='rows' /></strip></edge>
      </cards>
      <simple-id uuid='{ws1_uuid}' />
    </window>

    <window class='worksheet' name='Education Field Attrition'>
      <cards>
        <edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge>
        <edge name='top'><strip size='2147483647'><card type='columns' /></strip><strip size='2147483647'><card type='rows' /></strip></edge>
      </cards>
      <simple-id uuid='{ws2_uuid}' />
    </window>

    <window class='worksheet' name='OverTime Attrition Bar'>
      <cards>
        <edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge>
        <edge name='top'><strip size='2147483647'><card type='columns' /></strip><strip size='2147483647'><card type='rows' /></strip></edge>
      </cards>
      <simple-id uuid='{ws3_uuid}' />
    </window>

    <window class='worksheet' name='Income Slabs Bar Chart'>
      <cards>
        <edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge>
        <edge name='top'><strip size='2147483647'><card type='columns' /></strip><strip size='2147483647'><card type='rows' /></strip></edge>
      </cards>
      <simple-id uuid='{ws4_uuid}' />
    </window>

    <window class='dashboard' maximized='true' name='HR Analytics Executive Master Dashboard'>
      <cards>
        <edge name='left'><strip size='160'><card type='pages' /><card type='filters' /><card type='marks' /></strip></edge>
      </cards>
      <simple-id uuid='{dash_uuid}' />
    </window>
  </windows>
</workbook>
"""

    twbx_path = '/Users/bhagath/Desktop/AIO/Yuva_intern/HR_Analytics_Dashboard.twbx'
    csv_path = '/Users/bhagath/Desktop/AIO/Yuva_intern/HR_Analytics_Cleaned.csv'

    with zipfile.ZipFile(twbx_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Write .twb inside zip
        zf.writestr('HR_Analytics_Dashboard.twb', twb_content)
        # Embed data inside zip
        zf.write(csv_path, 'Data/HR_Analytics_Cleaned/HR_Analytics_Cleaned.csv')

    print(f"Successfully generated Tableau Packaged Workbook (.twbx) at: {twbx_path}")

if __name__ == "__main__":
    build_twbx()
