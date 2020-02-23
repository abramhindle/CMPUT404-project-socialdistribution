import React from 'react';
import { Layout } from 'antd';
import AdminHeader from './components/AdminHeader'
import AdminSideBar from './components/AdminSideBar';
import NodesContent from './components/NodesContent';

function NodesPage() {
  return (
    <div>
      <Layout>
        <AdminHeader/>
        <Layout>
            <AdminSideBar defaultSelectedKeys="MyNodes"/>
            <Layout style={{ padding: '12px 24px 24px'}}><NodesContent/></Layout>
        </Layout>
    </Layout>
    </div>
  );
}

export default NodesPage;