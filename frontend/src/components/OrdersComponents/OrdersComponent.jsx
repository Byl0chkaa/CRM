import React from 'react';
import OrderComponent from "./OrderComponent";

const OrdersComponent = ({orders, handleOrdering}) => {
    return (
        <div className="table-container">
            <table className="orders-table">
                <thead>
                    <tr>
                        <th onClick={() => handleOrdering('id')}>id</th>
                        <th onClick={() => handleOrdering('name')}>name</th>
                        <th onClick={() => handleOrdering('surname')}>surname</th>
                        <th onClick={() => handleOrdering('email')}>email</th>
                        <th onClick={() => handleOrdering('phone')}>phone</th>
                        <th onClick={() => handleOrdering('age')}>age</th>
                        <th onClick={() => handleOrdering('course')}>course</th>
                        <th onClick={() => handleOrdering('course_format')}>course_format</th>
                        <th onClick={() => handleOrdering('course_type')}>course_type</th>
                        <th onClick={() => handleOrdering('status')}>status</th>
                        <th onClick={() => handleOrdering('sum')}>sum</th>
                        <th onClick={() => handleOrdering('alreadyPaid')}>alreadyPaid</th>
                        <th onClick={() => handleOrdering('group')}>group</th>
                        <th onClick={() => handleOrdering('created_at')}>created_at</th>
                        <th onClick={() => handleOrdering('manager')}>manager</th>
                    </tr>
                </thead>
                <tbody>
                    {orders.map(order => (
                        <OrderComponent key={order.id} order={order} />
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default OrdersComponent;