import {apiService} from "./apiService";
import {urls} from "../constants/urls";

export const ordersService = {
    getAll: async (page = 1, order) => {
        return await apiService.get(urls.orders, {
            params: {
                page: page,
                order: order
            }
        });
    }
}