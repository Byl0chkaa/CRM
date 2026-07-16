import React, {useEffect, useState} from 'react';
import OrdersComponent from "../../components/OrdersComponents/OrdersComponent";
import PaginationComponent from "../../components/PaginationComponent/PaginationComponent";
import {ordersService} from "../../services/ordersService";
import './OrdersPage.css'
import {useSearchParams} from "react-router-dom";

const OrdersPage = () => {
    const [orders, setOrders] = useState([]);
    const [searchParams, setSearchParams] = useSearchParams();
    const [totalPages, setTotalPages] = useState(1);


    const currentPage = Number(searchParams.get('page')) || 1;
    const orderingParams = searchParams.get('order');
    useEffect(() => {
        ordersService.getAll(currentPage, orderingParams).then(({data}) => {
            setOrders(data.data);
            setTotalPages(data.total_pages);
        });
    }, [currentPage, orderingParams]);

    const handlePageChange = (newPage) => {
        searchParams.set('page', newPage)
        setSearchParams(searchParams);
    };

    const handleOrdering = (columnName) => {
        let newOrder = columnName;

        if (orderingParams === columnName){
            newOrder = `-${columnName}`
        }
        else if (orderingParams === `-${columnName}`){
            searchParams.delete('order');
            searchParams.set('page', 1);
            setSearchParams(searchParams)
            return;
        }
        searchParams.set('order', newOrder);
        searchParams.set('page', 1);
        setSearchParams(searchParams)
    }

    return (
        <div>
            <OrdersComponent orders={orders} handleOrdering={handleOrdering}/>
            <PaginationComponent
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={handlePageChange}
            />
        </div>
    );
};

export default OrdersPage;