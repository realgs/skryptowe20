import React from 'react'
import { Table, Typography } from 'antd';

const { Title } = Typography;
const columns = [
    {
        title: 'Date',
        dataIndex: 'date',
    },
    {
        title: 'Original sum',
        dataIndex: 'original_sum',
    },
    {
        title: 'Currency sum',
        dataIndex: 'currency_sum',
    },
];

export default function SummaryTable({ data }) {
    return (
        <>
            <Title level={5}>{data.currency}</Title>
            <Table columns={columns} dataSource={data.summary} scroll={{ y: 500 }} />
        </>
    )
}
