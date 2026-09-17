import os
import zipfile

def create_tableau_clustering_xml():
    # Write valid Tableau XML for HR_Analytics_Clustering_Dashboard.twb
    twb_content = """<?xml class='1.0' encoding='utf-8' ?>
<workbook original-version='18.1' source-build='2023.1.0' source-platform='mac' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
  <preferences>
    <preference name='ui.encoding.shelf.height' value='24' />
    <preference name='ui.shelf.height' value='26' />
  </preferences>
  <datasources>
    <datasource caption='HR Analytics Clustered' inline='true' name='federated.hr_clustered' version='18.1'>
      <connection class='federated'>
        <named-connections>
          <named-connection caption='HR_Analytics_Clustered' name='textscan.hr_clustered'>
            <connection class='textscan' directory='.' filename='HR_Analytics_Clustered.csv' password='' server='' />
          </named-connection>
        </named-connections>
      </connection>
      <column datatype='integer' name='[Cluster]' role='dimension' type='ordinal' />
      <column datatype='string' name='[Persona]' role='dimension' type='nominal' />
      <column datatype='string' name='[Attrition]' role='dimension' type='nominal' />
      <column datatype='string' name='[Department]' role='dimension' type='nominal' />
      <column datatype='integer' name='[Age]' role='measure' type='quantitative' />
      <column datatype='integer' name='[MonthlyIncome]' role='measure' type='quantitative' />
      <column datatype='integer' name='[TotalWorkingYears]' role='measure' type='quantitative' />
      <column datatype='integer' name='[YearsAtCompany]' role='measure' type='quantitative' />
      <column datatype='real' name='[PCA1]' role='measure' type='quantitative' />
      <column datatype='real' name='[PCA2]' role='measure' type='quantitative' />
      <layout dim-ordering='alphabetic' dim-percentage='0.5' measure-ordering='alphabetic' measure-percentage='0.5' show-structure='true' />
      <semantic-values>
        <semantic-value key='[Country].[Name]' value='&quot;United States&quot;' />
      </semantic-values>
    </datasource>
  </datasources>
  <worksheets>
    <worksheet name='Elbow Curve &amp; Clusters'>
      <table>
        <view>
          <datasources>
            <datasource caption='HR Analytics Clustered' name='federated.hr_clustered' />
          </datasources>
          <datasource-dependencies datasource='federated.hr_clustered'>
            <column datatype='string' name='[Persona]' role='dimension' type='nominal' />
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
        <rows>[federated.hr_clustered].[avg:MonthlyIncome:ql]</rows>
        <cols>[federated.hr_clustered].[avg:TotalWorkingYears:ql]</cols>
      </table>
    </worksheet>

    <worksheet name='2D PCA Projection'>
      <table>
        <view>
          <datasources>
            <datasource caption='HR Analytics Clustered' name='federated.hr_clustered' />
          </datasources>
          <datasource-dependencies datasource='federated.hr_clustered'>
            <column datatype='string' name='[Persona]' role='dimension' type='nominal' />
            <column datatype='real' name='[PCA1]' role='measure' type='quantitative' />
            <column datatype='real' name='[PCA2]' role='measure' type='quantitative' />
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
        <rows>[federated.hr_clustered].[avg:PCA2:ql]</rows>
        <cols>[federated.hr_clustered].[avg:PCA1:ql]</cols>
      </table>
    </worksheet>

    <worksheet name='Attrition by Persona'>
      <table>
        <view>
          <datasources>
            <datasource caption='HR Analytics Clustered' name='federated.hr_clustered' />
          </datasources>
          <datasource-dependencies datasource='federated.hr_clustered'>
            <column datatype='string' name='[Persona]' role='dimension' type='nominal' />
            <column datatype='string' name='[Attrition]' role='dimension' type='nominal' />
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
        <rows>[federated.hr_clustered].[none:Persona:nk]</rows>
        <cols>[federated.hr_clustered].[none:Attrition:nk]</cols>
      </table>
    </worksheet>
  </worksheets>

  <dashboards>
    <dashboard name='HR Workforce Clustering Executive Dashboard'>
      <style />
      <size maxheight='900' maxwidth='1400' minheight='700' minwidth='1000' />
      <zones>
        <zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>
          <zone h='98000' id='2' param='vert' type-v2='layout-flow' w='98000' x='1000' y='1000'>
            <zone h='10000' id='3' type-v2='text' w='98000' x='1000' y='1000'>
              <formatted-text>
                <run bold='true' fontcolor='#111827' fontsize='18'>HR Workforce Segmentation &amp; K-Means Clustering Dashboard</run>
              </formatted-text>
            </zone>
            <zone h='88000' id='4' param='horz' type-v2='layout-flow' w='98000' x='1000' y='11000'>
              <zone h='88000' id='5' name='Elbow Curve &amp; Clusters' w='49000' x='1000' y='11000' />
              <zone h='88000' id='6' name='2D PCA Projection' w='49000' x='50000' y='11000' />
            </zone>
          </zone>
        </zone>
      </zones>
    </dashboard>
  </dashboards>

  <windows>
    <window class='dashboard' name='HR Workforce Clustering Executive Dashboard'>
      <active pane-at-count='1' />
    </window>
  </windows>
</workbook>
"""
    
    twb_path = os.path.join(os.path.dirname(__file__), 'HR_Analytics_Clustering_Dashboard.twb')
    with open(twb_path, 'w', encoding='utf-8') as f:
        f.write(twb_content)
    print(f"Generated Tableau XML workbook: {twb_path}")

    # Build Packaged Tableau Workbook (.twbx)
    twbx_path = os.path.join(os.path.dirname(__file__), 'HR_Analytics_Clustering_Dashboard.twbx')
    csv_path = os.path.join(os.path.dirname(__file__), 'HR_Analytics_Clustered.csv')

    with zipfile.ZipFile(twbx_path, 'w', zipfile.ZIP_DEFLATED) as twbx:
        twbx.write(twb_path, arcname='HR_Analytics_Clustering_Dashboard.twb')
        if os.path.exists(csv_path):
            twbx.write(csv_path, arcname='Data/HR_Analytics_Clustered.csv')
    
    print(f"Generated Packaged Tableau workbook (.twbx): {twbx_path}")

if __name__ == '__main__':
    create_tableau_clustering_xml()
