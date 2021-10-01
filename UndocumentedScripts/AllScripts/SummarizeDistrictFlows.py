import xlsxwriter as xl
from xlsxwriter.utility import xl_rowcol_to_cell as rc2cell
import os
from dsa_util import *

base_path = r'T:\TIM_3.1\TIM_3.1_SocRecDistCalibration\scenario'
survey_path = os.path.join(base_path, 'DaySimSummaries', 'data') #Get relative filepaths for these to be used in VISUM
input_path = os.path.join(base_path, 'inputs')
output_path = os.path.join(base_path, 'Output')
summary_path = os.path.join(base_path, 'Reporting')

models = ['Work Location', 'School Location', 'Other Tour Destination']
order = ['Philadelphia', 'Suburban PA', 'Suburban NJ', 'Extended PA', 'Extended NJ', 'Extended DE/MD']
N = len(order)

outfile = os.path.join(summary_path, 'DistrictSummary.xlsx')

taz2district_file = r'D:\ref\taz2district.csv'
taz2district = pd.read_csv(taz2district_file, index_col = 0)['DISTRICT']

def read_coefs(coef_fp):
    f = open(coef_fp)
    coefs = f.read().split('\n')
    f.close()
    return coefs

def pivot_data(data, row, col, weight):
    global order
    N = len(order)
    outdata = pd.DataFrame(np.zeros((N, N)), order, order)#in the court
    grouped_data = data.groupby([row, col]).sum()[weight].reset_index()
    for i in grouped_data.index:
        record = grouped_data.loc[i]
        outdata.loc[record[row], record[col]] += record[weight]
    return outdata

def process_data(tables):
    global taz2district, order
    hhper = tables['hh'][['hhno', 'hhtaz']].merge(tables['per'][['hhno', 'pno', 'pwtaz', 'pstaz', 'psexpfac']], on = 'hhno')
    #Add household district
    hhper['hhdistrict'] = hhper['hhtaz'].map(taz2district)

    #Isolate workers and add work location district
    workers = hhper[hhper['pwtaz'] > 0]
    workers['pwdistrict'] = hhper['pwtaz'].map(taz2district)

    #Isolate students and add school location district
    students = hhper[hhper['pstaz'] > 0]
    students['psdistrict'] = hhper['pstaz'].map(taz2district)

    #Isolate other tours and add origin and destination districts
    hhtour = tables['hh'][['hhno']].merge(tables['tour'][['hhno', 'pdpurp', 'totaz', 'tdtaz', 'toexpfac']], on = 'hhno')
    other = hhtour[hhtour['pdpurp'] > 2]
    other['todistrict'] = other['totaz'].map(taz2district)
    other['tddistrict'] = other['tdtaz'].map(taz2district)

    #Pivot data
    outputs = {}
    outputs['Work Location'] = pivot_data(workers, 'hhdistrict', 'pwdistrict', 'psexpfac')
    outputs['School Location'] = pivot_data(students, 'hhdistrict', 'psdistrict', 'psexpfac')
    outputs['Other Tour Destination'] = pivot_data(other, 'todistrict', 'tddistrict', 'toexpfac')

    return outputs

def write_flow_table(data, sheet, name, startrow, startcol, formats):
    districts = data.index
    N = len(districts)
    sheet.write(startrow, startcol, name, formats['L'])
    sheet.write(startrow + N+1, startcol, 'Total', formats['L'])
    sheet.write(startrow, startcol + N+1, 'Total', formats['L'])
    for i in range(N):
        sheet.write(startrow + i+1, startcol, districts[i], formats['L'])
        sheet.write(startrow, startcol + i+1, districts[i], formats['L'])
        for j in range(N):
            sheet.write(startrow + i+1, startcol + j+1, data.loc[districts[i], districts[j]], formats['#'])
        sheet.write_formula(startrow + i+1, startcol + N+1,
                            '=SUM({0}:{1})'.format(rc2cell(startrow + i+1, startcol + 1), rc2cell(startrow + i+1, startcol + N)),
                            formats['#'])
        sheet.write_formula(startrow + N+1, startcol + i+1,
                            '=SUM({0}:{1})'.format(rc2cell(startrow + 1, startcol + i+1), rc2cell(startrow + N, startcol + i+1)),
                            formats['#'])
    sheet.write_formula(startrow + N+1, startcol + N+1,
                        '=SUM({0}:{1})'.format(rc2cell(startrow + 1, startrow + 1), rc2cell(startcol + N, startcol + N)),
                        formats['#'])

def write_share_table(data, sheet, name, startrow, startcol, refrow, refcol, formats):
    districts = data.index
    N = len(districts)
    sheet.write(startrow, startcol, name, formats['L'])
    sheet.write(startrow + N+1, startcol, 'Total', formats['L'])
    sheet.write(startrow, startcol + N+1, 'Total', formats['L'])
    for i in range(N):
        sheet.write(startrow + i+1, startcol, districts[i], formats['L'])
        sheet.write(startrow, startcol + i+1, districts[i], formats['L'])
    for i in range(N+1):
        for j in range(N+1):
            sheet.write_formula(startrow + i+1, startcol + j+1,
                                '=IFERROR({0}/{1},0)'.format(rc2cell(refrow + i+1, refcol + j+1), rc2cell(refrow + i+1, refcol + N+1)),
                                formats['%'])

def write_ratio_table(data, sheet, name, startrow, startcol, numrow, numcol, denrow, dencol, formats):
    districts = data.index
    N = len(districts)
    sheet.write(startrow, startcol, name, formats['L'])
    sheet.write(startrow + N+1, startcol, 'Total', formats['L'])
    sheet.write(startrow, startcol + N+1, 'Total', formats['L'])
    for i in range(N):
        sheet.write(startrow + i+1, startcol, districts[i], formats['L'])
        sheet.write(startrow, startcol + i+1, districts[i], formats['L'])
    for i in range(N+1):
        for j in range(N+1):
            sheet.write_formula(startrow + i+1, startcol + j+1,
                                '=IFERROR({0}/{1},1)'.format(rc2cell(numrow + i+1, numcol + j+1), rc2cell(denrow + i+1, dencol + j+1)),
                                formats['/'])

def write_adjustment_table(data, sheet, name, startrow, startcol, refrow, refcol, formats):
    districts = data.index
    N = len(districts)
    sheet.write(startrow, startcol, name, formats['L'])
    for i in range(N):
        sheet.write(startrow + i+1, startcol, districts[i], formats['L'])
        sheet.write(startrow, startcol + i+1, districts[i], formats['L'])
        for j in range(N):
            sheet.write_formula(startrow + i+1, startcol + j+1,
                                '=IFERROR(LN({0})-ln({1}), 0)'.format(rc2cell(refrow + i+1, refcol + j+1), rc2cell(refrow + i+1, refcol + i+1)),
                                formats['/'])

def write_tables(survey_data, daysim_data, sheet):
    write_flow_table(survey_data, sheet, 'Survey', 0, 0, formats)
    write_flow_table(daysim_data, sheet, 'DaySim', 0, N+3, formats)
    write_share_table(survey_data, sheet, 'Survey', 9, 0, 0, 0, formats)
    write_share_table(daysim_data, sheet, 'DaySim', 9, N+3, 0, N+3, formats)
    write_ratio_table(daysim_data, sheet, 'Ratio', 18, 0, 9, 0, 9, N+3, formats)
    write_adjustment_table(daysim_data, sheet, 'Adjustment', 18, N+3, 18, 0, formats)
    sheet.set_column(0, 2*N+4, 11)

#def write

print('Reading Survey Data')
survey = []
survey.append(DSTable('hh', os.path.join(survey_path, 'dvrpc_hrecx6.dat'), '\t'))
survey.append(DSTable('per', os.path.join(survey_path, 'dvrpc_precx6.dat'), '\t'))
survey.append(DSTable('tour', os.path.join(survey_path, 'dvrpc_tourx6.dat'), '\t'))
survey = ReadTables(survey)

print('Reading DaySim Data')
daysim = []
daysim.append(DSTable('hh', os.path.join(output_path, '_household_2.dat'), '\t'))
daysim.append(DSTable('per', os.path.join(output_path, '_person_2.dat'), '\t'))
daysim.append(DSTable('tour', os.path.join(output_path, '_tour_2.dat'), '\t'))
daysim = ReadTables(daysim)

print('Getting Flows')
survey_flows = process_data(survey)
daysim_flows = process_data(daysim)

print('Writing Workbook')
book = xl.Workbook(outfile)
number_format = book.add_format({'num_format': '#,##0'})
percent_format = book.add_format({'num_format': '0.0%'})
ratio_format = book.add_format({'num_format': '0.00'})
label_format = book.add_format({'bold': True})
formats = {'#': number_format, '%': percent_format, '/': ratio_format, 'L': label_format}

print('Writing Summaries')
for model in survey_flows:
    sheet = book.add_worksheet(model)
    write_tables(survey_flows[model], daysim_flows[model], sheet)

#sheet = book.get_worksheet_by_name('Work Location')
#work_location_coefs = read_coefs(os.path.join(input_path, 'Coefficients', 'WorkLocationCoefficients_LSM1_DVRPC_2015.F12'))
#school_location_coefs = read_coefs(os.path.join(input_path, 'Coefficients', 'SchoolLocationCoefficients_LSM1_DVRPC_2015.F12'))
#other_destination_coefs = read_coefs(os.path.join(input_path, 'Coefficients', 'OtherTourDestinationCoefficients_LSM1_DVRPC_2015.F12'))

book.close()


print('Done')