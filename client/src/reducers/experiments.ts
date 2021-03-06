import * as _ from 'lodash';
import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import { actionTypes, ExperimentAction } from '../actions/experiment';
import { ExperimentSchema } from '../constants/schemas';
import { STOPPED } from '../constants/statuses';
import { getExperimentIndexName } from '../constants/utils';
import { ExperimentModel, ExperimentsEmptyState, ExperimentStateSchema } from '../models/experiment';
import { GroupsEmptyState, GroupStateSchema } from '../models/group';
import { ProjectsEmptyState, ProjectStateSchema } from '../models/project';
import { LastFetchedNames } from '../models/utils';

export const experimentsReducer: Reducer<ExperimentStateSchema> =
  (state: ExperimentStateSchema = ExperimentsEmptyState, action: ExperimentAction) => {
    let newState = {...state};

    const processExperiment = (experiment: ExperimentModel) => {
      const uniqueName = getExperimentIndexName(experiment.unique_name);
      if (!_.includes(newState.lastFetched.names, uniqueName)) {
        newState.lastFetched.names.push(uniqueName);
      }
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      const normalizedExperiments = normalize(experiment, ExperimentSchema).entities.experiments;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName],
        ...normalizedExperiments[experiment.unique_name]
      };
      if (newState.byUniqueNames[uniqueName].jobs == null) {
        newState.byUniqueNames[uniqueName].jobs = [];
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.CREATE_EXPERIMENT:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames, [
              getExperimentIndexName(action.experiment.unique_name)]: action.experiment
          },
          uniqueNames: [...state.uniqueNames, getExperimentIndexName(action.experiment.unique_name)]
        };
      case actionTypes.DELETE_EXPERIMENT:
        return {
          ...state,
          uniqueNames: state.uniqueNames.filter(
            (name) => name !== getExperimentIndexName(action.experimentName)),
          lastFetched: {
            ...state.lastFetched,
            names: state.lastFetched.names.filter(
              (name) => name !== getExperimentIndexName(action.experimentName))},
        };
      case actionTypes.STOP_EXPERIMENT:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [getExperimentIndexName(action.experimentName)]: {
              ...state.byUniqueNames[getExperimentIndexName(action.experimentName)], last_status: STOPPED}
          },
        };
      case actionTypes.BOOKMARK_EXPERIMENT:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [getExperimentIndexName(action.experimentName)]: {
              ...state.byUniqueNames[getExperimentIndexName(action.experimentName)], bookmarked: true}
          },
        };
      case actionTypes.UNBOOKMARK_EXPERIMENT:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [getExperimentIndexName(action.experimentName)]: {
              ...state.byUniqueNames[getExperimentIndexName(action.experimentName)], bookmarked: false}
          },
        };
      case actionTypes.UPDATE_EXPERIMENT:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames, [
              getExperimentIndexName(action.experiment.unique_name)]: action.experiment
          }
        };
      case actionTypes.RECEIVE_EXPERIMENTS:
        newState.lastFetched = new LastFetchedNames();
        newState.lastFetched.count = action.count;
        for (const experiment of action.experiments) {
          newState = processExperiment(experiment);
        }
        return newState;
      case actionTypes.REQUEST_EXPERIMENTS:
        newState.lastFetched = new LastFetchedNames();
        return newState;
      case actionTypes.RECEIVE_EXPERIMENT:
        return processExperiment(action.experiment);
      default:
        return state;
    }
  };

export const ProjectExperimentsReducer: Reducer<ProjectStateSchema> =
  (state: ProjectStateSchema = ProjectsEmptyState, action: ExperimentAction) => {
    let newState = {...state};

    const processExperiment = function(experiment: ExperimentModel) {
      const uniqueName = getExperimentIndexName(experiment.unique_name);
      const projectName = experiment.project;
      if (_.includes(newState.uniqueNames, projectName) &&
        !_.includes(newState.byUniqueNames[projectName].experiments, uniqueName)) {
        newState.byUniqueNames[projectName].experiments.push(uniqueName);
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.RECEIVE_EXPERIMENT:
        return processExperiment(action.experiment);
      case actionTypes.RECEIVE_EXPERIMENTS:
        for (const experiment of action.experiments) {
          newState = processExperiment(experiment);
        }
        return newState;
      default:
        return state;
    }
  };

export const GroupExperimentsReducer: Reducer<GroupStateSchema> =
  (state: GroupStateSchema = GroupsEmptyState, action: ExperimentAction) => {
    let newState = {...state};

    const processExperiment = function(experiment: ExperimentModel) {
      const uniqueName = getExperimentIndexName(experiment.unique_name);
      const groupName = experiment.experiment_group;
      if (groupName != null &&
        _.includes(newState.uniqueNames, groupName) &&
        !_.includes(newState.byUniqueNames[groupName].experiments, uniqueName)) {
        newState.byUniqueNames[groupName].experiments.push(uniqueName);
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.RECEIVE_EXPERIMENT:
        return processExperiment(action.experiment);
      case actionTypes.RECEIVE_EXPERIMENTS:
        for (const experiment of action.experiments) {
          newState = processExperiment(experiment);
        }
        return newState;
      default:
        return state;
    }
  };
