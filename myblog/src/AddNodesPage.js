import React from 'react';
import { Layout } from 'antd';
import AdminHeader from './components/AdminHeader'
import AdminSideBar from './components/AdminSideBar';
import AddNodesContent from './components/AddNodesContent';

function AddNodesPage() {
  return (
    <div>
        <Layout>
            <AdminHeader></AdminHeader>
            <Layout>
                <AdminSideBar defaultSelectedKeys="None"></AdminSideBar>
                <Layout><AddNodesContent /></Layout>
            </Layout>
        </Layout>
    </div>
  );
}

export default AddNodesPage;