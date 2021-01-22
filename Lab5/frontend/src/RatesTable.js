import React from 'react'
import { Table, Typography } from 'antd';

const { Title } = Typography;
const columns = [
  {
    title: 'Date',
    dataIndex: 'date',
  },
  {
    title: 'Value',
    dataIndex: 'value',
  },
  {
    title: 'Interpolated',
    dataIndex: 'interpolated',
  },
];

export default function RatesTable({ data }) {

  return (
    <>
      <Title level={5}>{data.currency}</Title>
      <Table columns={columns} dataSource={data.rates} scroll={{ y: 500 }} />
    </>
  )
}
