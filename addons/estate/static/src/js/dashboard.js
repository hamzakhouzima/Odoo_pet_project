/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, onWillStart } from "@odoo/owl";

class Dashboard extends Component {
    static template = "estate.DashboardTemplate";
    static props = {};
    
    setup() {
        // Use the service locator pattern to get services
        this.orm = useService("orm");
        this.userService = useService("user");
        
        this.state = useState({
            data: [],
            user: this.userService.context
        });
        
        onWillStart(async () => {
            await this.loadData();
        });
    }
    
    async loadData() {
        try {
            // Use ORM service instead of direct RPC
            this.state.data = await this.orm.call(
                'estate.property',  // Replace with your actual model name
                'get_dashboard_data',  // Custom method in your model
                []
            );
        } catch (error) {
            console.error("Failed to load data:", error);
            this.state.data = [];
        }
    }
    
    async createRecord() {
        try {
            await this.orm.call(
                'estate.property',
                'create_dashboard_record',
                [{ name: "New", value: 100 }]
            );
            await this.loadData();
        } catch (error) {
            console.error("Failed to create record:", error);
        }
    }
    
    async updateRecord(id) {
        try {
            await this.orm.call(
                'estate.property',
                'write',
                [[id], { value: 200 }]
            );
            await this.loadData();
        } catch (error) {
            console.error("Failed to update record:", error);
        }
    }
    
    async deleteRecord(id) {
        try {
            await this.orm.call(
                'estate.property',
                'unlink',
                [[id]]
            );
            await this.loadData();
        } catch (error) {
            console.error("Failed to delete record:", error);
        }
    }
}
function dashboardAction(env, action) {
    return {
        component: Dashboard,
        props: { action },
    };
}


// Register the action
registry.category("actions").add("estate_property_dashboard", {
    component: Dashboard,
});